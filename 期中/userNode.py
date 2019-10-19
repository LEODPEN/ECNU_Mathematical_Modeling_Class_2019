import math
from random import random as rd

class UserNode:

    # 初始化未获取消息且应该递增
    def __init__(self, graph, id):
        self.graph = graph
        self.id = id
        self.interest = rd()
        self.know = False  # 初始未获取消息
        self.radius = -1
        self.timeToKnow = 0
        self.isWait = False

    def isForward(self, strength):
        return math.sqrt(self.interest*strength)+0.5  # 既然大部分是美国本土 4 时区

    def timeToKnowForFollower(self, distance): # 以时区刻画的距离
        if self.radius == 0:  # 那么则是转发就立马看见
            self.radius = 1
        return int(distance*distance/self.radius)  # 单位为小时

    def hearNews(self, alreadyKnownAccount):
        self.know = True
        print(str(self.id)+"获得消息")
        return alreadyKnownAccount+1

    def setTimeToKnow(self, timeToKnow):
        self.timeToKnow = timeToKnow

    def shareNews(self, toBeInformedSet, alreadyKnownAccount, timeUnit):
        for follower in self.graph.neighbors(self):
            if rd() <= self.isForward(self.graph[self][follower]["weight"][0]):   # 是否传播
                if not follower.know:
                    timeToKnow = timeUnit + self.timeToKnowForFollower(self.graph[self][follower]["weight"][1])
                    # if timeToKnow == 0:
                    #     follower.setTimeToKnow(timeUnit)
                    #     alreadyKnownAccount = follower.hearNews(alreadyKnownAccount)
                    #     toBeInformedSet.put(follower)
                    # else:

                    if not follower.isWait:
                        follower.setTimeToKnow(timeToKnow)
                        follower.isWait = True
                        toBeInformedSet.put(follower)
                # else:
                #     timeToKnow = self.timeToKnowForFollower(self.graph[self][follower]["weight"][1])
                #     if timeToKnow == 0:
                #         follower.setTimeToKnow(timeUnit)
                #         alreadyKnownAccount = follower.hearNews(alreadyKnownAccount)
                #         toBeInformedSet.put(follower)
                #     else:
                #         if timeToKnow < follower.timeToKnow:
                #             follower.setTimeToKnow(timeUnit+timeToKnow)
                #             toBeInformedSet.put(follower)
        return alreadyKnownAccount

    def __cmp__(self, other):
        if self.timeToKnow < other.timeToKnow:
            return -1
        elif self.timeToKnow == other.timeToKnow:
            if self.id > other.id:
                return 1
            return -1
        return 1

    def __lt__(self, other):
        return self.timeToKnow < other.timeToKnow or (self.timeToKnow == other.timeToKnow and self.id < other.id)

    def __gt__(self, other):
        return self.timeToKnow > other.timeToKnow or (self.timeToKnow == other.timeToKnow and self.id > other.id)




