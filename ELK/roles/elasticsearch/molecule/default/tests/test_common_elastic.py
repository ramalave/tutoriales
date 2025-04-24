import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
  os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('elastic')


# Check - Installing ElasticSearch latest version
def test_elasticsearch_is_installed(host):
  elasticsearch = host.package("elasticsearch")
  assert elasticsearch.is_installed

# Check - Configuring ElasticSearch
@pytest.mark.parametrize('files', [
  ("/etc/elasticsearch/elasticsearch.yml")
])
def test_config_elasticsearch_exists(host, files):
  file = host.file(files)
  assert file.exists
  assert file.user == 'root'
  assert file.group == 'root'
  assert file.mode == 0o644

# Check - Create a service drop-in configuration directory
@pytest.mark.parametrize('directories', [
  ("/etc/systemd/system/elasticsearch.service.d")
])
def test_elasticsearch_config_directory_exists(host, directories):
  directory = host.file(directories)
  assert directory.exists
  assert directory.mode == 0o755

# Check - Configuring systemd service time out
@pytest.mark.parametrize('files', [
  ("/etc/systemd/system/elasticsearch.service.d/startup-timeout.conf")
])
def test_systemd_config_timeout_elasticsearch_exists(host, files):
	file = host.file(files)
	assert file.exists
	assert file.user == 'root'
	assert file.group == 'root'
	assert file.mode == 0o644

# Check - Service ElasticSearch enabled, unmasked, started
def test_service_elasticsearch_enabled_unmasked_started(host):
	elasticsearch = host.service("elasticsearch")
	assert elasticsearch.is_enabled
	assert elasticsearch.is_masked == False
	assert elasticsearch.is_running

# Check - Generating users
def test_generating_users(host):
	assert host.run_expect([78],"/usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto -b")