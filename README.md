# Project-1-JWKS-server
**Objective:**
Develop a RESTful JWKS server that provides public keys with unique identifiers (kid) for verifying JSON Web Tokens (JWTs), implements key expiry for enhanced security, includes an authentication endpoint, and handles the issuance of JWTs with expired keys based on a query parameter.

**Requirements**

**1. Key Generation**
Implement RSA key pair generation.
Associate a Key ID (kid) and expiry timestamp with each key.

**2. Web server with two handlers**
Serve HTTP on port 8080
A RESTful JWKS endpoint that serves the public keys in JWKS format.
Only serve keys that have not expired.
A /auth endpoint that returns an unexpired, signed JWT on a POST request.
If the “expired” query parameter is present, issue a JWT signed with the expired key pair and the expired expiry.

**3. Documentation**
Code should be organized.
Code should be commented where needed.
Code should be linted per your language/framework.

**4. Tests**
Test suite for your given language/framework with tests for you.
Test coverage should be over 80%.

**5. Blackbox testing**
Ensure the included test clientLinks to an external site. functions against your server.
The testing client will attempt a POST to /auth with no body. There is no need to check authentication for this project.
