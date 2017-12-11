import boto3
aws_access_key='AKIAIQB6PY73S2ZRCA3Q'
aws_access_pass='qXxZyQsqNv2W3NGLpGyTNyma7/5PSDNezDaPiFf1'
s3=boto3.client('s3',aws_access_key_id=aws_access_key,aws_secret_access_key=aws_access_pass)


import gdax, time
class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["LTC-USD","ETH-USD","BTC-USD"]
        self.message_count = 0
        self.msg_list=[]
        print("Lets count the messages!")
    def on_message(self, msg):
        
        
        if 'price' in msg and 'type' in msg and msg['type']=="match": #(msg['type']=="received" or msg['type']=="match"):
            self.message_count += 1
            self.msg_list.extend([msg])
    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)



import json
while True:
    wsClient.message_count=0
    wsClient.msg_list=[]
    while (wsClient.message_count < 1000):
        #print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
        #print (len(wsClient.msg_list))
        time.sleep(1)
    tnow=str(int(time.time()))
    print (tnow,'Dumping batch')
    data=json.dumps(wsClient.msg_list)
    key='gdax/'+'gdax_'+tnow+'.json'
    s3.put_object(Bucket='udi-crypto',Key=key, Body=data)

