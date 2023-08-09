resource "google_monitoring_dashboard" "performance_dashboard" {
  dashboard_json = <<EOF
  {
    "displayName": "Performance Dashboard",
    "gridLayout": {
      "widgets": [
        {
          "title": "GKE scheduler scheduling attempts",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"prometheus.googleapis.com/scheduler_schedule_attempts_total/counter\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_DELTA"
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE scheduler pending pods",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"prometheus.googleapis.com/scheduler_pending_pods/gauge\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_COUNT",
                      "crossSeriesReducer": "REDUCE_COUNT",
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE container restart count",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/restart_count\" resource.type=\"k8s_container\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_DELTA",
                    
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE container CPU request utilization",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/cpu/request_utilization\" resource.type=\"k8s_container\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_MAX",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE container CPU limit utilization",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/cpu/limit_utilization\" resource.type=\"k8s_container\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_MAX",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE container memory request utilization",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/memory/request_utilization\" resource.type=\"k8s_container\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_MAX",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE container memory limit utilization",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/memory/limit_utilization\" resource.type=\"k8s_container\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_MAX",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GCE instance bytes written",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"compute.googleapis.com/instance/disk/write_bytes_count\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_SUM",
                      "crossSeriesReducer": "REDUCE_SUM",
                      "groupByFields": [
                        "resource.label.\"instance_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GCE instance bytes read",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"compute.googleapis.com/instance/disk/read_bytes_count\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_SUM",
                      "crossSeriesReducer": "REDUCE_SUM",
                      "groupByFields": [
                        "resource.label.\"instance_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GCE instance disk read operations",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"compute.googleapis.com/instance/disk/read_ops_count\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_SUM",
                      "crossSeriesReducer": "REDUCE_SUM",
                      "groupByFields": [
                        "resource.label.\"instance_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GCE instance disk write operations",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"compute.googleapis.com/instance/disk/write_ops_count\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_SUM",
                      "crossSeriesReducer": "REDUCE_SUM",
                      "groupByFields": [
                        "resource.label.\"instance_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "Cumulative CPU usage used by cores on GKE node",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/node/cpu/core_usage_time\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_RATE",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"node_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "Cumulative memory bytes used by GKE node",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/node/memory/used_bytes\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_SUM",
                      "crossSeriesReducer": "REDUCE_SUM",
                      "groupByFields": [
                        "resource.label.\"node_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE node % allocated memory utilization",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/node/memory/allocatable_utilization\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_MAX",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"node_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE node % allocated CPU utilization",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/node/cpu/allocatable_utilization\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_MAX",
                      "crossSeriesReducer": "REDUCE_MAX",
                      "groupByFields": [
                        "resource.label.\"node_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "GKE Container Uptime",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"kubernetes.io/container/uptime\" resource.type=\"k8s_container\"",
                    "aggregation": {
                      "alignmentPeriod":"60s",
                      "perSeriesAligner":"ALIGN_SUM",
                      "crossSeriesReducer": "REDUCE_SUM",
                      "groupByFields": [
                        "resource.label.\"container_name\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
        {
          "title": "Total number of requests per GKE service",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "plotType": "LINE",
                "targetAxis": "Y1",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"prometheus.googleapis.com/nginx_ingress_controller_requests/counter\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_DELTA",
                      "crossSeriesReducer": "REDUCE_PERCENTILE_95",
                      "groupByFields": [
                        "metric.label.\"service\"",
                        "metric.label.\"status\"",
                        "metric.label.\"method\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        },
       {
          "title": "Request latency per GKE service",
          "xyChart": {
            "dataSets": [
              {
                "minAlignmentPeriod": "60s",
                "timeSeriesQuery": {
                  "timeSeriesFilter": {
                    "filter": "metric.type=\"prometheus.googleapis.com/nginx_ingress_controller_request_duration_seconds/histogram\"",
                    "aggregation": {
                      "alignmentPeriod": "60s",
                      "perSeriesAligner": "ALIGN_DELTA",
                      "crossSeriesReducer": "REDUCE_PERCENTILE_95",
                      "groupByFields": [
                        "metric.label.\"service\"",
                        "metric.label.\"status\"",
                        "metric.label.\"method\""
                      ]
                    }
                  }
                }
              }
            ]
          }
        }
     ]
   }
 }
 EOF
}
