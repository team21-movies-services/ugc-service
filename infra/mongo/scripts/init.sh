#!/usr/bin/env bash

echo "Waiting for startup.."
wait_for_it () {
    until mongosh --host ${mongo_host} --eval 'quit(db.runCommand({ ping: 1 }).ok ? 0 : 2)' &>/dev/null; do
    printf '.'
    sleep 1
    done
}

echo "Started.."

echo "Setup config server 1 = mongocfg1"
mongo_host=mongocfg1
wait_for_it
mongosh --host mongocfg1 <<EOF
rs.initiate(
    {
        _id: "mongors1conf",
        configsvr: true,
        members: [
            { _id: 0, host: "mongocfg1"},
            { _id: 1, host: "mongocfg2"},
            { _id: 2, host: "mongocfg3"}
        ]
    }
)
EOF


echo "Setup shard 1 = mongors1n1"
mongo_host=mongors1n1
wait_for_it
mongosh --host mongors1n1 <<EOF
rs.initiate(
    {
        _id: "mongors1",
        members: [
            { _id: 0, host: "mongors1n1" },
            { _id: 1, host: "mongors1n2" },
            { _id: 2, host: "mongors1n3" }
        ]
    }
)
EOF


echo "Setup router 1 = mongos1 (add shard)"
mongo_host=mongos1
wait_for_it
mongosh --host mongos1 --eval 'sh.addShard("mongors1/mongors1n1")'

echo "Setup shard 2 = mongors2n1"
mongo_host=mongors2n1
wait_for_it

mongosh --host mongors2n1 <<EOF
rs.initiate(
    {
        _id: "mongors2",
        members: [
            { _id: 0, host: "mongors2n1" },
            { _id: 1, host: "mongors2n2" },
            { _id: 2, host: "mongors2n3" }
        ]
    }
)
EOF

echo "Setup router 2 = mongos1 (add shard)"
mongo_host=mongos2
wait_for_it

mongosh --host mongos2 --eval 'sh.addShard("mongors2/mongors2n1")'

echo "Setup database, add sharding, add collection and shard collection by field"
mongo_host=mongos1
wait_for_it

mongosh --host mongos1 <<EOF
    use ${MONGO_DB_NAME};
    sh.enableSharding('${MONGO_DB_NAME}');
    db.createCollection('${MONGO_DB_NAME}.${MONGO_COLLECTION_NAME}');
    sh.shardCollection('${MONGO_DB_NAME}.${MONGO_COLLECTION_NAME}', {'${MONGO_SHARD_FIELD}': 'hashed'});
EOF

