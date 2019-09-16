import json
from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool, NTLM, ALL_ATTRIBUTES, MODIFY_REPLACE

# LDAP_SERVER_POOL = ["192.168.0.xxx", "192.168.1.xxx"]

AUTH_LDAP_SERVER_URI = "ldap://corpad.glb.intel.com"
LDAP_SERVER_PORT = 3268
ADMIN_DN = "cn=TSIE LDAP,ou=DC,ou=MCG TSIE,ou=Resources,dc=ccr,dc=corp,dc=intel,dc=com"
ADMIN_PASSWORD = "intel123!"
SEARCH_BASE = "ou=Workers,dc=ccr,dc=corp,dc=intel,dc=com"

# AUTH_LDAP_BIND_DN = "cn=TSIE LDAP,ou=DC,ou=MCG TSIE,ou=Resources,dc=ccr,dc=corp,dc=intel,dc=com"
# AUTH_LDAP_BIND_PASSWORD = "intel123!"


def ldap_auth(username, password):
    # ldap_server_pool = ServerPool(LDAP_SERVER_POOL)
    server = Server(AUTH_LDAP_SERVER_URI, port=LDAP_SERVER_PORT, get_info=ALL, use_ssl=True, connect_timeout=1800)
    conn = Connection(
        server,
        user=ADMIN_DN,
        password=ADMIN_PASSWORD,
        auto_bind=True,
        # authentication=NTLM,
        check_names=True,
        lazy=False,
        raise_exceptions=False)

    conn.open()
    conn.bind()

    res = conn.search(
        search_base = SEARCH_BASE,
        search_filter='(sAMAccountName={})'.format(username),
        # search_filter='(objectclass=user)',
        # search_filter="(objectclass=organizationalUnit)",
        search_scope = SUBTREE,
        attributes=ALL_ATTRIBUTES,
        paged_size = 2
    )


    ret = conn.response_to_json()
    print(ret)

    if res:
        entry = conn.response[0]
        dn = entry['dn']
        print(dn)
        attr_dict = entry['attributes']

       # check password by dn
        try:
            conn2 = Connection(server, user=dn, password=password, check_names=True, lazy=False, raise_exceptions=False)
            conn2.bind()
            if conn2.result["description"] == "success":
                print((True, attr_dict["mail"], attr_dict["sAMAccountName"], attr_dict["givenName"]))
                return (True, attr_dict["mail"], attr_dict["sAMAccountName"], attr_dict["givenName"])
            else:
                print("auth fail")
                return (False, None, None, None)
        except Exception as e:
            print("auth fail")
            return (False, None, None, None)
    else:
        return (False, None, None, None)

if __name__ == "__main__":
    ldap_auth("chenxudx", "JIUER0-9")
    # ldap_auth()