~/.docker/config.json:
add proxy: `host.docker.internal:7890`

```
{
	"auths": {
		"https://index.docker.io/v1/": {}
	},
	"credsStore": "desktop",
	"proxies": {
		"default": {
			"httpProxy": "http://host.docker.internal:7890",
			"httpsProxy": "http://host.docker.internal:7890",
			"noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
		}
	},
	"currentContext": "desktop-linux",
	"plugins": {
		"-x-cli-hints": {
			"enabled": "true"
		}
	},
	"features": {
		"hooks": "true"
	}
}```