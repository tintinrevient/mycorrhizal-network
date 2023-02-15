CREATE SINK CONNECTOR `traffic_to_neo4j` WITH(
	"topics" = 'traffic',
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
    "neo4j.topic.cypher.traffic" = 'MERGE (src:Host{ip: event.ip_src}) MERGE (dst:Host{ip: event.ip_dst}) MERGE (src)-[r:TO]->(dst) ON CREATE SET r.count=0, src.country=event.country_src, src.city=event.city_src, src.latitude=event.latitude_src, src.longitude=event.longitude_src, dst.country=event.country_dst, dst.city=event.city_dst, dst.latitude=event.latitude_dst, dst.longitude=event.longitude_dst ON MATCH SET r.count=r.count+1, src.country=event.country_src, src.city=event.city_src, src.latitude=event.latitude_src, src.longitude=event.longitude_src, dst.country=event.country_dst, dst.city=event.city_dst, dst.latitude=event.latitude_dst, dst.longitude=event.longitude_dst'
);