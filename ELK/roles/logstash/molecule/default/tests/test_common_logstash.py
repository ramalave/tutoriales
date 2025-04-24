import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
  os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('logstash')

# File with all define pipelines - Should be the same value at 'ansible/ELK/roles/logstash/defaults/main.yml', can be change for different tests
path_pipelines_config = ''

# Check - Installing Logstash latest version
def test_logstash_is_installed(host):
  logstash = host.package("logstash")
  assert logstash.is_installed

# Check - Configuring Logstash
@pytest.mark.parametrize('files', [
  ("/etc/logstash/logstash.yml")
])
def test_config_logstash_exists(host, files):
  file = host.file(files)
  assert file.exists
  assert file.user == 'root'
  assert file.group == 'root'
  assert file.mode == 0o644

# Check - Configuring Logstash Pipelines
#@pytest.mark.parametrize('files', [
#  ("/etc/logstash/conf.d/")
#])
#def test_config_logstash_pipelines_exists(host, files):
#  if path_pipelines_config == '':
#    file = host.file(files)
#    assert file.exists
#    assert file.user == 'root'
#    assert file.group == 'root'
#    assert file.mode == 0o644

# Check - Configuring Logstash Pipelines
@pytest.mark.parametrize('files', [
  ("/etc/logstash/pipelines.yml")
])
def test_config_logstash_pipelines_file_exists(host, files):
  if path_pipelines_config != '':
    file = host.file(files)
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 0o644

# Check - Service Logstash enabled, unmasked, started
def test_service_logstash_enabled_unmasked_started(host):
	logstash = host.service("logstash")
	assert logstash.is_enabled
	assert logstash.is_masked == False
	assert logstash.is_running
