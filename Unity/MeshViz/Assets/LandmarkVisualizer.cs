using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LandmarkVisualizer : MonoBehaviour
{
    [SerializeField] private TCPTestClient _client;
    [SerializeField] private float _scale = 1f;
    public Transform _Finger;

    Dictionary<int, string> handPoints = new Dictionary<int, string>()
    {
        {0, "WRIST"},
        {1, "THUMB_CMC"},
        {2, "THUMB_MCP"},
        {3, "THUMB_IP"},
        {4, "THUMB_TIP"},
        {5, "INDEX_FINGER_MCP"},
        {6, "INDEX_FINGER_PIP"},
        {7, "INDEX_FINGER_DIP"},
        {8, "INDEX_FINGER_TIP"},
        {9, "MIDDLE_FINGER_MCP"},
        {10, "MIDDLE_FINGER_TIP"},
        {11, "MIDDLE_FINGER_DIP"},
        {12, "MIDDLE_FINGER_TIP"},
        {13, "RING_FINGER_MCP"},
        {14, "RING_FINGER_PIP"},
        {15, "RING_FINGER_DIP"},
        {16, "RING_FINGER_TIP"},
        {17, "PINKY_MCP"},
        {18, "PINKY_PIP"},
        {19, "PINKY_DIP"},
        {20, "PINKY_TIP"}
    };



    private void OnDrawGizmos()
    {
        if (_client.Landmarks != null)
        {
            foreach (var l in _client.Landmarks)
            {
                _Finger.transform.position = new Vector3(l.x, l.y, l.z) * _scale;
                print(handPoints[l.point]);
            }
        }
    }
}
