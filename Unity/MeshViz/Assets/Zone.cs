using UnityEngine;

public class Zone : MonoBehaviour
{
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "Object")
            print("Connected");
    }
}
