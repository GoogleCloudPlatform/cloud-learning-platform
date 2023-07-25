locals {
  nginx_ingress_kubernetes_io_cors_allow_origin = join(",", flatten([
    "https://${var.web_app_domain}",
    "https://${var.ckt_app_domain}",
    "http://localhost:4200",
    var.additional_nginx_cors_allow_origin,
  ]))
}


module "cert_manager" {
  source = "terraform-iaac/cert-manager/kubernetes"

  cluster_issuer_email                   = var.cert_issuer_email
  cluster_issuer_name                    = "letsencrypt"
  cluster_issuer_private_key_secret_name = "cert-manager-private-key"

  additional_set = var.enable_certman_gcr_io_images ? [
    {
      name  = "repository"
      value = "gcr.io/cloud-marketplace/google/cert-manager"
    },
    {
      name  = "tag"
      value = "1.7"
    }
  ] : []
}

resource "kubernetes_namespace" "ingress_nginx" {
  metadata {
    name = "ingress-nginx"
  }
}

resource "google_compute_address" "ingress_ip_address" {
  name = "nginx-controller"
}

module "nginx-controller" {
  source    = "terraform-iaac/nginx-controller/helm"
  version   = "2.0.2"
  namespace = "ingress-nginx"

  ip_address = google_compute_address.ingress_ip_address.address

  # TODO: does this require cert_manager up and running or can they be completed in parallel
  depends_on = [
    module.cert_manager, resource.kubernetes_namespace.ingress_nginx
  ]
}

resource "kubectl_manifest" "ingress" {
  count     = var.create_nginx_ingress ? 1 : 0
  yaml_body = <<YAML
kind: Ingress
apiVersion: networking.k8s.io/v1
metadata:
  name: learning-platform-nginx-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt"
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-methods: "PUT, GET, POST, OPTIONS, DELETE"
    nginx.ingress.kubernetes.io/cors-allow-origin: ${local.nginx_ingress_kubernetes_io_cors_allow_origin}
    nginx.ingress.kubernetes.io/cors-allow-credentials: "true"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-body-size: "500m"
spec:
  tls:
    - hosts:
      - ${var.api_domain}
      secretName: learning-platform-backend-ssl-cert
  rules:
  - host: ${var.api_domain}
    http:
      paths:
      - path: /session
        pathType: Prefix
        backend:
          service:
            name: session
            port:
              number: 80
      - path: /dashboard
        pathType: Prefix
        backend:
          service:
            name: dashboard
            port: 
              number: 80
      - path: /authentication
        pathType: Prefix
        backend:
          service:
            name: authentication
            port: 
              number: 80
      - path: /messages
        pathType: Prefix
        backend:
          service:
            name: messages
            port: 
              number: 80
      - path: /notes
        pathType: Prefix
        backend:
          service:
            name: notes
            port: 
              number: 80
      - path: /utils
        pathType: Prefix
        backend:
          service:
            name: utils
            port: 
              number: 80
      - path: /docs
        pathType: Prefix
        backend:
          service:
            name: api-docs
            port: 
              number: 80
      - path: /course_ingestion
        pathType: Prefix
        backend:
          service:
            name: course-ingestion
            port: 
              number: 80
      - path: /extractive_summarization
        pathType: Prefix
        backend:
          service:
            name: extractive-summarization
            port: 
              number: 80
      - path: /title_generation
        pathType: Prefix
        backend:
          service:
            name: title-generation
            port: 
              number: 80
      - path: /answer_a_question
        pathType: Prefix
        backend:
          service:
            name: answer-a-question
            port: 
              number: 80
      - path: /choose_the_fact
        pathType: Prefix
        backend:
          service:
            name: choose-the-fact
            port: 
              number: 80
      - path: /const_parsing
        pathType: Prefix
        backend:
          service:
            name: const-parsing
            port: 
              number: 80
      - path: /dialog_systems
        pathType: Prefix
        backend:
          service:
            name: dialog-systems
            port: 
              number: 80
      - path: /masked_word_prediction
        pathType: Prefix
        backend:
          service:
            name: masked-word-prediction
            port: 
              number: 80
      - path: /paraphrasing_practice
        pathType: Prefix
        backend:
          service:
            name: paraphrasing-practice
            port: 
              number: 80
      - path: /answer_a_question_evaluation
        pathType: Prefix
        backend:
          service:
            name: answer-a-question-evaluation
            port: 
              number: 80
      - path: /missed_text_templatize
        pathType: Prefix
        backend:
          service:
            name: feedback
            port: 
              number: 80
      - path: /assessment_items
        pathType: Prefix
        backend:
          service:
            name: assessment-items
            port: 
              number: 80
      - path: /coref_resolution
        pathType: Prefix
        backend:
          service:
            name: coref-resolution
            port: 
              number: 80
      - path: /grafana
        pathType: Prefix
        backend:
          service:
            name: kube-prometheus-stack-grafana
            port: 
              number: 80
      - path: /enhanced_feedback
        pathType: Prefix
        backend:
          service:
            name: enhanced-feedback
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
      - path: /triple_extraction
        pathType: Prefix
        backend:
          service:
            name: triple-extraction
            port: 
              number: 80
      - path: /lti
        pathType: Prefix
        backend:
          service:
            name: lti
            port: 
              number: 80
      - path: /skill-service
        pathType: Prefix
        backend:
          service:
            name: skill-service
            port: 
              number: 80
      - path: /matching-engine
        pathType: Prefix
        backend:
          service:
            name: matching-engine
            port: 
              number: 80
      - path: /learner-profile-service
        pathType: Prefix
        backend:
          service:
            name: student-learner-profile
            port: 
              number: 80
      - path: /erps-store
        pathType: Prefix
        backend:
          service:
            name: erps-store
            port: 
              number: 80
      - path: /recommendation-service
        pathType: Prefix
        backend:
          service:
            name: recommendation-service
            port: 
              number: 80
      - path: /assessment-service
        pathType: Prefix
        backend:
          service:
            name: assessment-service
            port: 
              number: 80
      - path: /knowledge-service
        pathType: Prefix
        backend:
          service:
            name: knowledge-service
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
      - path: /prior-learning-assessment
        pathType: Prefix
        backend:
          service:
            name: prior-learning-assessment
            port: 
              number: 80
      - path: /rules-engine
        pathType: Prefix
        backend:
          service:
            name: rules-engine
            port: 
              number: 80
      - path: /notification
        pathType: Prefix
        backend:
          service:
            name: notification
            port:
              number: 80
YAML

  depends_on = [
    module.nginx-controller
  ]

}
