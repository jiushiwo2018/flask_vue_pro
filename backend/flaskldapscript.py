from flask_ldap3_login import LDAP3LoginManager

config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostname of your LDAP Server
config['LDAP_HOST'] = "ldap://corpad.glb.intel.com"
config['LDAP_PORT'] = 3268
config['LDAP_USE_SSL'] = True
config['LDAP_ALWAYS_SEARCH_BIND'] = True
config['LDAP_READONLY'] = False
# config['LDAP_BIND_DIRECT_CREDENTIALS'] = True
# Base DN of your directory
config['LDAP_BASE_DN'] = "DC=ccr,DC=corp,DC=intel,DC=com"

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'OU=Workers'

# Groups DN to be prepended to the Base DN
# config['LDAP_GROUP_DN'] = 'ou=groups'

# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
# config['LDAP_USER_LOGIN_ATTR'] = 'mail'

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = "cn=TSIE LDAP,ou=DC,ou=MCG TSIE,ou=Resources,dc=ccr,dc=corp,dc=intel,dc=com"

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = "intel123!"

# Setup a LDAP3 Login Manager.
ldap_manager = LDAP3LoginManager()

# Init the mamager with the config since we aren't using an app
ldap_manager.init_config(config)

# Check if the credentials are correct
response = ldap_manager.authenticate('Chen, XudongX', 'JIUER0-9')


print(response.status, response.user_dn, response.user_info)