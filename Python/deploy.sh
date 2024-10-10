VERSION=$(.venv/bin/python -c 'import atlasapprox; print(atlasapprox.__version__)' | tail -n 1)
.venv/bin/twine upload dist/atlasapprox-${VERSION}* -u __token__ -p $(<pypi.token)
