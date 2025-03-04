from ray import serve


@serve.deployment(route_prefix="/test", num_replicas=2, ray_actor_options={
    "runtime_env": {"pip": ["pandas"]}
})
class TestDeployment:
    async def __call__(self, request):
        return "Hello World!"


app = TestDeployment.bind()
