======
Docker
======


Install:

    curl -sSL https://get.docker.com/ | sh


     .. code-block:: shell

        $ docker build -t GOApy:1.1.0 .

        $ docker run --rm goapy:1.1.0
        [ (0, {'app': False, 'db': False, 'vpc': False}),
          (1, {'app': False, 'db': False, 'vpc': True}),
          (2, {'app': False, 'db': True, 'vpc': True}),
          (3, {'app': False, 'db': 'started', 'vpc': True}),
          (4, {'app': False, 'db': 'stopped', 'vpc': True}),
          (5, {'app': False, 'db': 'not_health', 'vpc': True}),
          (6, {'app': True, 'db': True, 'vpc': True}),
          (7, {'app': 'stopped', 'db': True, 'vpc': True}),
          (8, {'app': 'started', 'db': True,

