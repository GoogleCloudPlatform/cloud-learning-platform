module "stackdriver_adapter" {
    source = "../stackdriver_adapter"
    
    count = var.lms_enabled || var.enable_stackdriver_adapter ? 1 : 0
    project_id = var.project_id
    
    depends_on = [
        module.gke.gke_cluster_id
    ]
}
