#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## Frank@Villaro-Dixon.eu - DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE, etc.

import kopf
import kubernetes

NODE_SELECTOR_ANNOTATION_NAME = 'frankkkkk.nodeSelectorDuringExecution'

def get_node_labels(v1_api, node_name):
    '''Return a dict of nodes with their corresponding labels'''

    node = v1_api.read_node(node_name)
    return node.metadata.labels


def get_pods_of_node(v1_api, node_name):
    field_selector = 'spec.nodeName='+node_name
    return v1_api.list_pod_for_all_namespaces(field_selector=field_selector).items


def is_pod_nodeSelector_fails(pod, node_labels):
    if pod.status.phase != 'Running':
        return False

    pod_selectors = pod.spec.node_selector

    for label, value in pod_selectors.items():
        if node_labels.get(label, None) != value:
            return True
    return False


def ensure_pods_of_node(node_name, node_labels):
    kubernetes.config.load_incluster_config()
    v1_api = kubernetes.client.CoreV1Api()


    node_labels = get_node_labels(v1_api, node_name)

    for pod in get_pods_of_node(v1_api, node_name):
        annotations = pod.metadata.annotations
        if annotations is None:
            continue

        nsde = annotations.get(NODE_SELECTOR_ANNOTATION_NAME, '')
        if nsde == 'true':
            # We ask that we check nodeSelector on execution for this pod
            if is_pod_nodeSelector_fails(pod, node_labels):
                pod_name = pod.metadata.name
                pod_namespace = pod.metadata.namespace
                v1_api.delete_namespaced_pod(pod_name, pod_namespace)
                print(f'Pod {pod_namespace}/{pod_name} not satisfying nodeSelector labels. will be killed 🔫')



@kopf.on.update('', 'v1', 'nodes')
def node_update_handler(spec, old, new, diff, body, **args):
    node_name = body['metadata']['name']
    node_labels = body['metadata']['labels']

    for changed in diff:
        what = changed[1]
        if what[0:2] == ('metadata', 'labels'):
            ensure_pods_of_node(node_name, node_labels)
            break


# vim: set ts=4 sw=4 et:

