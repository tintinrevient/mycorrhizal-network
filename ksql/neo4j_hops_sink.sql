CREATE SINK CONNECTOR `hops_to_neo4j` WITH(
	"topics" = 'hops',
    "connector.class" = 'streams.kafka.connect.sink.Neo4jSinkConnector',
    "key.converter" = 'org.apache.kafka.connect.json.JsonConverter',
    "key.converter.schemas.enable" = 'false',
    "value.converter" = 'org.apache.kafka.connect.json.JsonConverter',
    "value.converter.schemas.enable" = 'false',
    "errors.retry.timeout" = '-1',
    "errors.retry.delay.max.ms" = '1000',
    "errors.tolerance" = 'all',
    "errors.log.enable" = 'true',
    "errors.log.include.messages" = 'true',
    "neo4j.server.uri" = 'bolt://neo4j:7687',
    "neo4j.authentication.basic.username" = 'neo4j',
    "neo4j.authentication.basic.password" = 'password',
    "neo4j.topic.cypher.hops" = 'MERGE (src:Hop{ip: event.prev_hop}) MERGE (dst:Hop{ip: event.curr_hop}) MERGE (src)-[r:TO]->(dst) ON CREATE SET r.count=1, src.count=1, dst.count=1 ON MATCH SET r.count=r.count+1, src.count=src.count+1, dst.count=dst.count+1'
);