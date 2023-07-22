resource "google_compute_global_address" "ingress_gclb_ip_address" {
  name = "ingress-gclb"
}


# TODO: switch to hashicorp k8s provider, use side by side
# k2tf
resource "kubectl_manifest" "managed_certificate" {
  yaml_body = <<YAML
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: gclb-managed-cert
spec:
  domains:
    - ${var.api_domain}
YAML
}


resource "kubectl_manifest" "ingress" {
  yaml_body = <<YAML
kind: Ingress
apiVersion: networking.k8s.io/v1
metadata:
  name: learning-platform-gclb-ingress
  annotations:
    kubernetes.io/ingress.global-static-ip-name: ${google_compute_global_address.ingress_gclb_ip_address.name}
    networking.gke.io/managed-certificates: ${kubectl_manifest.managed_certificate.name}
    kubernetes.io/ingress.class: "gce"
    networking.gke.io/v1beta1.FrontendConfig: ${kubectl_manifest.frontend_config.name}

spec:
  rules:
  - host: ${var.api_domain}
    http:
      paths:
      - path: /*
        pathType: ImplementationSpecific
        backend:
          service:
            name: lms-admin-ui
            port:
              number: 80
      - path: /lms
        pathType: Prefix
        backend:
          service:
            name: lms
            port:
              number: 80
      - path: /lti
        pathType: Prefix
        backend:
          service:
            name: lti
            port:
              number: 80
      - path: /classroom-shim
        pathType: Prefix
        backend:
          service:
            name: classroom-shim
            port:
              number: 80
      - path: /authentication
        pathType: Prefix
        backend:
          service:
            name: authentication
            port:
              number: 80
      - path: /llm-service
        pathType: Prefix
        backend:
          service:
            name: llm-service
            port:
              number: 80
      - path: /learner-profile-service
        pathType: Prefix
        backend:
          service:
            name: student-learner-profile
            port:
              number: 80
      - path: /assessment-service
        pathType: Prefix
        backend:
          service:
            name: assessment-service
            port:
              number: 80
      - path: /learning-object-service
        pathType: Prefix
        backend:
          service:
            name: learning-object-service
            port:
              number: 80
      - path: /learning-record-service
        pathType: Prefix
        backend:
          service:
            name: learning-record-service
            port:
              number: 80
      - path: /user-management
        pathType: Prefix
        backend:
          service:
            name: user-management
            port:
              number: 80
      - path: /rules-engine
        pathType: Prefix
        backend:
          service:
            name: rules-engine
            port:
              number: 80
      - path: /prior-learning-assessment
        pathType: Prefix
        backend:
          service:
            name: prior-learning-assessment
            port:
              number: 80
      - path: /docs
        pathType: Prefix
        backend:
          service:
            name: api-docs
            port:
              number: 80
      - path: /dashboard
        pathType: Prefix
        backend:
          service:
            name: dashboard
            port:
              number: 80
      - path: /extractive_summarization
        pathType: Prefix
        backend:
          service:
            name: extractive-summarization
            port:
              number: 80
      - path: /deep_knowledge_tracing
        pathType: Prefix
        backend:
          service:
            name: deep-knowledge-tracing
            port:
              number: 80
      - path: /item_response_theory
        pathType: Prefix
        backend:
          service:
            name: item-response-theory
            port:
              number: 80
      - path: /utils
        pathType: Prefix
        backend:
          service:
            name: utils
            port:
              number: 80
YAML
}

resource "kubectl_manifest" "frontend_config" {
  yaml_body = <<YAML
apiVersion: networking.gke.io/v1beta1
kind: FrontendConfig
metadata:
  name: ingress-security-config
spec:
  sslPolicy: ${google_compute_ssl_policy.gke-ingress-ssl-policy.name}
  redirectToHttps:
    enabled: true
YAML
}

resource "google_compute_ssl_policy" "gke-ingress-ssl-policy" {
  name            = "gke-ingress-ssl-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}
