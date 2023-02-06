## Required environment variables

LTI Service requires a pair of rsa private and public keys for signing the jwt token (also referred as lti_message in LTI documentation) and a issuer url.

A pair of RSA private and public keys can be generated using the `generate_rsa_keys.py` script found in the utils folder.

For running this service, a set of RSA public and private keys are picked with the terms `lti-service-public-key` and `lti-service-private-key` from gcp secret manager.

The issuer url is the domain where the LTI service will be hosted. This will be passed as `iss` claim in the lti_message. This should also be passed as an environment variable with the name `LTI_ISSUER_DOMAIN`. If not passed as env variable, the default `http://localhost` will be used for `iss` claim.


## Moodle setup

Currently for testing the development of lti service for both, 'as a tool' and 'as a platform', we are using open source platform moodle. We can deploy a fresh moodle instance using helm-chart and skaffold.

To deploy moodle on gke, you can use below skaffold.yaml

```yaml
apiVersion: skaffold/v2beta13
kind: Config
metadata:
  name: moodle
deploy:
    helm:
      releases:
      - name: moodle
        repo: https://charts.bitnami.com/bitnami
        remoteChart: moodle
        setValues:
          moodleUsername: user
          moodlePassword: Test@1234
        #   service.type: NodePort # uncomment if needed to link with ingress
profiles:
- name: dev
```

Deploying moodle without providing `service.type` will expose an ip address on which you can find moodle running.
