local shortport = require "shortport"
local http = require "http"

description = [[
This script identifies systems that use Wildfly. For more information about Wildfly, visit http://wildfly.org/ and for more
information about Wildfly Exploitation, visit https://github.com/hlldz/wildPwn.
]]

---
-- @usage
-- nmap --script wildfly-detect <host>
--
-- @output
-- PORT      STATE SERVICE
-- 80/tcp    open  http
-- |_wildfly-detect: Wildfly Detected!
-- 135/tcp   open  msrpc
-- 139/tcp   open  netbios-ssn
-- 443/tcp   open  https
-- |_wildfly-detect: Wildfly Detected!
-- 445/tcp   open  microsoft-ds
-- 8080/tcp  open  http-proxy
-- |_wildfly-detect: Wildfly Detected!
-- 8443/tcp  open  https-alt
-- |_wildfly-detect: Wildfly Detected!
---

author = "Halil DALABASMAZ | artofpwn.com"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"discovery", "intrusive"}

portrule = shortport.http

action = function(host, port)

    	local uri = "/"
    	local response = http.get(host, port, uri)

    	local options = {header={}}
        options['header']['User-Agent'] = "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"

    	if ( response.status == 200 )
    	then
      		local wildfly = string.match(response.body, "[Ww][Ee][Ll][Cc][Oo][Mm][Ee][Tt][Oo][Ww][Ii][Ll][Dd][Ff][Ll][Yy]")
            	return "Wildfly Detected!"
	else
		return "Down"
    	end
end
