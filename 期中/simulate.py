import networkx as nx
from random import random as rd
from queue import PriorityQueue as pq
import matplotlib.pyplot as plt
from userNode import UserNode

LIMIT = 1000
M = 5000
P_avg = 15
M_received = 5  # 初始有20个知道消息
TIME_DISTANCE = 24
graph = nx.DiGraph()
nodes = []  # 一共5000
toBeInformedSet = pq()


def init(alreadyKnownAccount):
    # 初始化得知消息情况
    for i in range(M_received):
        node = nodes[int(M * rd())]
        alreadyKnownAccount = node.hearNews(alreadyKnownAccount)
        alreadyKnownAccount = node.shareNews(toBeInformedSet, alreadyKnownAccount, 0)
    return alreadyKnownAccount


# step 1：对用户网络建模

def buildUserNetwoks():

    # N(2.5,4) => (x-2.5)/2~N(0,1)
    # [-,1],[1,2],[2,3],[3,4],[4,+]
    p1 = 1 - 0.7734
    p2 = 1 - 0.5987
    p3 = 0.5987
    p4 = 0.7734


    # 存所有节点并加入list
    for i in range(M):
        user = UserNode(graph, i)
        graph.add_node(user)
        nodes.append(user)

    # 加边和赋予权重
    for node in nodes:
        for i in range(P_avg):
            follower = nodes[int(M * rd())]

            # 计算距离
            if rd() < 0.5:
                distance = int(4*rd())
            else:
                distance = int(TIME_DISTANCE*rd())

            if distance > node.radius:
                node.radius = distance
            if distance > follower.radius:
                follower.radius = distance

            # 计算关系稳定度
            prob = rd()
            if prob <= p1:
                strength = 1/5
            elif prob <= p2:
                strength = 2/5
            elif prob <= p3:
                strength = 3/5
            elif prob <= p4:
                strength = 4/5
            else:
                strength = 5/5
            # 加边
            graph.add_edge(node, follower, weight=(strength, distance))
            # 绘图用
            # graph.add_edge(node, follower, weight=distance)
    # nx.draw(graph,node_size=5)
    # plt.show()


# step 2：模拟传播
def propagation():
    t_start = 0
    t_end = 0
    t = t_start
    buildUserNetwoks()
    alreadyKnownAccount = 0
    alreadyKnownAccount = init(alreadyKnownAccount)

    while t < LIMIT:
        while not toBeInformedSet.empty():
            toBeInformedNode = toBeInformedSet.get()
            if t == toBeInformedNode.timeToKnow:
                if toBeInformedNode.know:
                    continue
                else:
                    alreadyKnownAccount = toBeInformedNode.hearNews(alreadyKnownAccount)
                    alreadyKnownAccount = toBeInformedNode.shareNews(toBeInformedSet, alreadyKnownAccount, t)
            else:
                toBeInformedSet.put(toBeInformedNode)
                break
        if alreadyKnownAccount >= 0.9 * M:
            t_end = t
            break
        print("当前时间:", t)
        t += 1
        print(str(alreadyKnownAccount))
    print("传播花费时间:", t_end - t_start)


if __name__ == "__main__":
    propagation()















