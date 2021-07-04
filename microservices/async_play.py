from asyncio import get_event_loop

class Task:
    def __init__(self, name):
        self.name = name
        self.result = 'success'
    
    async def run(self):
        print('doing', self.name)
        await asyncio.sleep(1)
        return self

class Pipeline:
    def __init__(self, name):
        self.name = name
        self.steps = []

async def monitor(q:Queue):
    while True:
        if q.empty():
            print('queue is empty')
            break
        pipeline = q.get()
        loop.create_task(pipeline_runner(pipeline))
        # in that case they run sequentially \ that's called coroutine chaining
        # await pipeline_runner(pipeline)


async def pipeline_runner(pipeline):
    for step in pipeline.steps:
        r = await step.run()
        if r.result == 'failed':
            print('failed pipeline', pipeline.name)
            break
        else:
            print('from pipeline {} got result {}'.format(pipeline.name, r.result))
            continue

q = Queue()

p1 = Pipeline('pipeline-1')
p1.steps.append(Task('enter the building'))
p1.steps.append(Task('take the money'))
p1.steps.append(Task('exit the building'))

p2 = Pipeline('pipeline-2')
p2.steps.append(Task('run the engine'))
p2.steps.append(Task('ride your bike'))
p2.steps.append(Task('sleep'))

p3 = Pipeline('pipeline-3')
p3.steps.append(Task('sit on pc'))
p3.steps.append(Task('eat'))
p3.steps.append(Task('sit again on pc'))

q.put(p1)
q.put(p2)
q.put(p3)

loop = get_event_loop()
loop.create_task(monitor(q))
loop.run_forever()
