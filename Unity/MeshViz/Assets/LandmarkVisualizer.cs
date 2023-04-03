using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LandmarkVisualizer : MonoBehaviour
{
    [Tooltip("Поместите в _client объект, получающий данные по сокетам")]
    [Header("Включите отображение gizmos")]
    [SerializeField] private TCPTestClient _client;
    [SerializeField] private float _scale = 1f;

    private void OnDrawGizmos()
    {
        if (_client.Landmarks != null)
        {
            foreach (var l in _client.Landmarks)
            {
                Gizmos.color = new Color(l.Visibility, l.Visibility, l.Visibility);
                Gizmos.DrawSphere(l.Position * _scale, 0.5f);
            }
        }
    }
}
