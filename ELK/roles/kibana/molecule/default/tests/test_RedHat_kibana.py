import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
  os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('kibana-centos')

# Check - Add elastic repo
@pytest.mark.parametrize('files', [
  ("/etc/yum.repos.d/elastic-7.x.repo")
])
def test_elastic_repo_exists(host, files):
	file = host.file(files)
	assert file.exists
