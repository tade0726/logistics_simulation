import simpy


def user(name, env, res, prio, preempt):
    with res.request(priority=prio, preempt=preempt) as req:
        try:
            print('%s requesting at %d' % (name, env.now))
            yield req
            print('%s got resource at %d' % (name, env.now))
            yield env.timeout(3)
        except simpy.Interrupt:
            print('%s got preempted at %d' % (name, env.now))
            # 重新请求资源
            env.process(user(name, env, res, prio, preempt))

env = simpy.Environment()
res = simpy.PreemptiveResource(env, capacity=1)
A = env.process(user('A', env, res, prio=0, preempt=True))
env.run(until=1) # Give A a head start
# B = env.process(user('B', env, res, prio=-2, preempt=False))
C = env.process(user('C', env, res, prio=-1, preempt=True))
env.run()
