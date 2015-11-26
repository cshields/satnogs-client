from flask import Flask, render_template

from satnogsclient import settings as client_settings
from satnogsclient.scheduler import scheduler
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    """View list of satnogs-client settings."""
    filters = [
        lambda x: not x.startswith('_'),
        lambda x: x.isupper()
    ]

    entries = client_settings.__dict__.items()
    settings = filter(lambda (x, y): all(f(x) for f in filters), entries)

    ctx = {
        'settings': sorted(settings, key=lambda x: x[0])
    }

    return render_template('index.j2', **ctx)


@app.route("/observations")
def observations():
    """View list of queued observation jobs."""
    observations = []
    for obs in scheduler.get_jobs():
        if obs.name == "spawn_observer":
            obs.kwargs['obj']['start'] = '{:%Y-%m-%d %H:%M}'.format(
                datetime.strptime(obs.kwargs['obj']['start'], '%Y-%m-%dT%H:%M:%SZ'))
            obs.kwargs['obj']['end'] = '{:%Y-%m-%d %H:%M}'.format(
                datetime.strptime(obs.kwargs['obj']['end'], '%Y-%m-%dT%H:%M:%SZ'))
            obs.kwargs['obj']['frequency'] = '{:.3f}'.format(
                obs.kwargs['obj']['frequency'] / 1000000.0)
            observations.append(obs)

    return render_template('observations.j2', observations=observations)
