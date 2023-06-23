"""sript for visualizing topic tree using neo4j"""
import json
from collections import defaultdict
from py2neo import Graph
import requests
from absl import flags, app
# pylint: disable=redefined-builtin,redefined-outer-name,broad-exception-raised
FLAGS = flags.FLAGS
flags.DEFINE_string("level", None, "level of the root node")
flags.DEFINE_string("id", None, "id of the root node")

flags.mark_flag_as_required("level")
flags.mark_flag_as_required("id")


def get_topic_tree(level, id):
  """returns topic tree for a given level and id"""
  try:
    # pylint: disable=line-too-long
    prediction = json.loads(
        requests.get(
            url="http://0.0.0.0:80/course_ingestion/api/v1/topic_tree/?level={}&id={}"
            .format(level, id)).content)["data"]
    return prediction
  except ConnectionError as e:
    raise Exception("failed to connect with \
        course ingestion microservice") from e
  except (TypeError, KeyError) as e:
    raise Exception("Internal server error") from e


url = "bolt://3.231.213.198:7687"  # bolt url
username = "neo4j"  # Default by neo4j
password = "accident-cord-practices"  # your db password


def generate_query(data, relation, graph):
  """generates a cypgher query to load a complete tree to neo4jdb"""
  if relation == "has_competency":
    query = """UNWIND $datas AS data
    MERGE (n:Learning_content_item {name:data.node1.title, id: data.node1.id})
    MERGE (m:Competency {name:data.node2.title, id: data.node2.id})
    MERGE (n)-[:RELATION {V:data.relation}]->(m)
    """
  elif relation == "has_sub_competency":
    query = """UNWIND $datas AS data
    MERGE (n:Competency {name:data.node1.title, id: data.node1.id})
    MERGE (m:Sub_competency {name:data.node2.title, id: data.node2.id})
    MERGE (n)-[:RELATION {V:data.relation}]->(m)
    """
  elif relation == "has_learning_objective":
    query = """UNWIND $datas AS data
    MERGE (n:Sub_competency {name:data.node1.title, id: data.node1.id})
    MERGE (m:Learning_objective {name:data.node2.title, id: data.node2.id})
    MERGE (n)-[:RELATION {V:data.relation}]->(m)
    """
  else:
    query = """UNWIND $datas AS data
    MERGE (n:Learning_objective {name:data.node1.title, id: data.node1.id})
    MERGE (m:Learning_unit {name:data.node2.title, id: data.node2.id})
    MERGE (n)-[:RELATION {V:data.relation}]->(m)
    """
  graph.run(query, {"datas": data})


def create_neo4j_graph(learning_content, url, username, password):
  """Create a neo4j graph using the ckg constructed from get_documents()."""
  graph = Graph(url, auth=(username, password))
  graph.delete_all()
  data = defaultdict(list)
  for competency in learning_content["competencies"]:
    data["competency"].append({
        "node1": {
            "title": learning_content["title"],
            "id": learning_content["id"]
        },
        "node2": {
            "title": competency["title"],
            "id": competency["id"]
        },
        "relation": "has_competency"
    })
    for sub_competency in competency["sub_competencies"]:
      data["sub_competency"].append({
          "node1": {
              "title": competency["title"],
              "id": competency["id"]
          },
          "node2": {
              "title": sub_competency["title"],
              "id": sub_competency["id"]
          },
          "relation": "has_sub_competency"
      })
      for lo in sub_competency["learning_objectives"]:
        data["lo"].append({
            "node1": {
                "title": sub_competency["title"],
                "id": sub_competency["id"]
            },
            "node2": {
                "title": lo["title"],
                "id": lo["id"]
            },
            "relation": "has_learning_objective"
        })
        for lu in lo["learning_units"]:
          data["lu"].append({
              "node1": {
                  "title": lo["title"],
                  "id": lo["id"]
              },
              "node2": {
                  "title": lu["title"],
                  "id": lu["id"]
              },
              "relation": "has_learning_unit"
          })
  generate_query(data["competency"], "has_competency", graph)
  generate_query(data["sub_competency"], "has_sub_competency", graph)
  generate_query(data["lo"], "has_learning_objective", graph)
  generate_query(data["lu"], "has_learning_unit", graph)
  print("database populated successfully.")


def main(argv):
  """neo4j visualization"""
  del argv
  learning_content = get_topic_tree(FLAGS.level, FLAGS.id)
  print("Fetched topic tree. Populating database!!")
  create_neo4j_graph(learning_content, url, username, password)


if __name__ == "__main__":
  app.run(main)
