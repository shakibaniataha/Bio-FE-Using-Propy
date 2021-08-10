from propy.PyPro import GetProDes
import MySQLdb
import json

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="propy_features")

cursor = db.cursor()

with open('output_fasta.txt', 'r') as f:
    counter = 0
    while True:
        try:
            protein_id = next(f).strip().split('>')[1]
            protein_seq = next(f).strip()

            des = GetProDes(protein_seq)
            features_dict = des.GetDPComp()  # AAC (Dipeptide Composition)
            protein_features = features_dict.values()
            features_json = json.dumps(protein_features)

            sql = "INSERT INTO protein (protein_id, features_json) VALUES (%s, %s)"
            val = (protein_id, features_json)
            cursor.execute(sql, val)

            db.commit()

            counter += 1
            print counter

        except StopIteration:
            break
