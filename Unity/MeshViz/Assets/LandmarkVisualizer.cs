using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LandmarkVisualizer : MonoBehaviour
{
    [Tooltip("Поместите в _client объект, получающий данные по сокетам")]
    [Header("Включите отображение gizmos")]
    [SerializeField] private TCPTestClient _client;
    [SerializeField] private float _scale = 1f;
    public GameObject _Obj;

    private void OnDrawGizmos()
    {
        if (_client.Landmarks != null)
        {
            foreach (var l in _client.Landmarks)
            {
                _Obj.gameObject.tag = "Object";
                _Obj.transform.position = l.Position * _scale;
            }
        }
    }

    

}
