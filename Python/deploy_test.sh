VERSION=$(.venv/bin/python -c 'import atlasapprox; print(atlasapprox.__version__)' | tail -n 1)
.venv/bin/twine upload -r testpypi dist/atlasapprox-${VERSION}* -u __token__ -p $(<testpypi.token)
