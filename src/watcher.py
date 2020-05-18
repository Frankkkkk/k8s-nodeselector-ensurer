#!/usr/bin/env python3
# frank.villaro@infomaniak.com - DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE, etc.

import time
import kubernetes


def get_node_labels(v1_api):
    '''Return a dict of nodes with their corresponding labels'''
    node_labels = {}
    ln = v1_api.list_node()
    for node in ln.items:
        name = node.metadata.name
        labels = node.metadata.labels
        node_labels[name] = labels

    return node_labels


def is_pod_nodeSelector_fails(pod, node_labels):
    if pod.status.phase != 'Running':
        return False



    pod_selectors = pod.spec.node_selector

    pod_elected_node = pod.spec.node_name
    labels_of_node = node_labels.get(pod_elected_node, {})

    for label, value in pod_selectors.items():
        if labels_of_node.get(label, None) != value:
            return True
    return False


def evict_pods_if_necessary(v1_api, node_labels):
    pod_list = v1_api.list_pod_for_all_namespaces()
    for pod in pod_list.items:
        annotations = pod.metadata.annotations
        if annotations == None:
            annotations = {}

        nsde = annotations.get('frankkkkk.nodeSelectorDuringExecution', '')
        if nsde == 'true':
            # We ask that we check nodeSelector on execution for this pod
            if is_pod_nodeSelector_fails(pod, node_labels):
                pod_name = pod.metadata.name
                pod_namespace = pod.metadata.namespace
                v1_api.delete_namespaced_pod(pod_name, pod_namespace)
                print(f'Pod {pod_namespace}/{pod_name} not satisfying nodeSelector labels. will be killed 🔫')



def main_loop():
    kubernetes.config.load_incluster_config()
    v1_api = kubernetes.client.CoreV1Api()

    while True:
        node_labels = get_node_labels(v1_api)
        evict_pods_if_necessary(v1_api, node_labels)
        time.sleep(60)


if __name__ == '__main__':
    main_loop()


# vim: set ts=4 sw=4 et:

