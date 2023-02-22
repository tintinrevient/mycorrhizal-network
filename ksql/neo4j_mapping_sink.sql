CREATE SINK CONNECTOR `mapping_to_neo4j` WITH(
	"topics" = 'mapping',
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
    "neo4j.topic.cypher.mapping" = 'MERGE (h:DNS{ip: event.ip, url: event.url}) ON CREATE SET h.count=1 ON MATCH SET h.count=h.count+1 MERGE (p:Host{ip: event.ip}) MERGE (p)-[:HAS_DNS]->(h)'
);