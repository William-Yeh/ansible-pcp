
williamyeh.pcp for Ansible Galaxy
============


## Summary

Role name in Ansible Galaxy: **[williamyeh.pcp](https://galaxy.ansible.com/list#/roles/4162)**

This Ansible role has the following features for [PCP (Performance Co-Pilot)](http://pcp.io):

 - Install PCP.
 - Install specified Performance Metrics Domain Agents (PMDAs).
 - Bare bone configuration (*real* configuration should be left to user's template files; see **Usage** section below).



## Role Variables

### Mandatory variables

Variables needed to be defined in user's playbook: None.


### Optional variables

User-configurable defaults:

```yaml
# an array of PMDAs to be activated
pcp_pmda


# path of pmcd.conf;
# default: '/etc/pcp/pmcd/pmcd.conf'
pcp_pmcdconf_path
```



## Handlers

- `restart pcp`

- `stop pcp`




## Usage


### Step 1: add role

Add role name `williamyeh.pcp` to your playbook file.


### Step 2: add variables, if any

Set vars in your playbook file.

Simple example:

```yaml
---
# file: simple-playbook.yml

- hosts: all
  sudo: True

  roles:
    - williamyeh.pcp

  vars:
    pcp_pmda:
      - summary
      - trace
```


## Dependencies

None.


## License

Licensed under the Apache License V2.0. See the [LICENSE file](LICENSE) for details.
