class LocalStoreg:

    def __init__(self):
        self.user_id = {}
        self.topic_id = {}
        self.name = {}

    def updateUserId(self, host, user_id):
        self.user_id.update({host: user_id})    
    
    def getUserId(self, host):
        user_id = self.user_id.get(host, None)
        print('user_id: ', user_id)
        return user_id
    
    def updateTopicId(self, user_id, topic_id):
        self.user_id.update({user_id: topic_id})
    
    def getTopicId(self, user_id):
        topic_id = self.user_id.get(user_id, None)
        print('topic_id: ', topic_id)
        return topic_id
    
    def updateName(self, user_id, name):
        self.name.update({user_id: name})
    
    def getName(self, user_id):
        name = self.name.get(user_id, None)
        print('topic_id: ', name)
        return name