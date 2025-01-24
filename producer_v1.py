from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient

# Protobuf class imports (generated from protoc)
from protos_v1.test_proto_pb2 import TestProto

# Schema Registry configuration
schema_registry_conf = {'url': 'http://localhost:18081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Create serializers for Protobuf
serializer = ProtobufSerializer(TestProto, schema_registry_client, {'use.deprecated.format': False})

producer_conf = {
    'bootstrap.servers': 'localhost:19092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': serializer
}

# Send Schema V1
msg_v1 = TestProto(property_a="AA", property_b="BB")
producer = SerializingProducer(producer_conf)
producer.produce(topic="example_topic", key="key1", value=msg_v1)
producer.flush()