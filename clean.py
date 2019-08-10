import sys
import rancher
from kubernetes import client, config
from kubernetes.client.rest import ApiException

delete_psptpbs = False

cluster_id = ""

access=sys.argv[1]
secret=sys.argv[2]
rancherurl=sys.argv[3]

for key, arg in enumerate(sys.argv):
    if arg == "-d":
        delete_psptpbs = True
    if arg == "-c":
        cluster_id = sys.argv[key+1]

rclient = rancher.Client(url=rancherurl + "/v3",
                        access_key=access,
                        secret_key=secret)


projects = rclient.list_project()

config.load_kube_config()
custom_api = client.CustomObjectsApi()

def just_project(proj):
    fragments = str.split(proj, ":")
    return fragments[len(fragments) - 1]


def just_cluster(proj):
    fragments = str.split(proj, ":")
    return fragments[0]

project_id_set = set(map(lambda x: just_project(x.id), projects))

psptpbs = rclient.list_pod_security_policy_template_project_binding()

for psptpb in psptpbs:
    proj_id = just_project(psptpb.targetProjectId)
    clus_id = just_cluster(psptpb.targetProjectId)

    if (proj_id not in project_id_set) and (cluster_id == "" or clus_id == cluster_id):
        if delete_psptpbs:
            print("deleting psptpb:", psptpb.name)
            try:
                custom_api.delete_namespaced_custom_object("management.cattle.io", "v3", clus_id, "podsecuritypolicytemplateprojectbindings", psptpb.name, client.V1DeleteOptions())
            except ApiExcept as e:
                print(e)
                print(psptpb.name, "failed to delete")
        else:
            print("remnant psptpb:", psptpb.name)

