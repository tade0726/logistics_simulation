import simpy


def user(name, env, res, prio=0):
    with res.request(priority=prio,) as req:
        try:
            print('%s requesting at %d' % (name, env.now))
            yield req
            print('%s got resource at %d' % (name, env.now))
            yield env.timeout(3)
        except simpy.Interrupt:
            print('%s got preempted at %d' % (name, env.now))
            # 重新请求资源
            env.process(user(name, env, res, prio,))

env = simpy.Environment()
res = simpy.PriorityResource(env, capacity=1)
A = env.process(user('A', env, res,))
B = env.process(user('B', env, res, prio=-1,))
C = env.process(user('C', env, res, prio=-10))
env.run()
