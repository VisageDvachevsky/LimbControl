using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;
using System.Text;

public class FingerController : MonoBehaviour
{
    // ����� � ���� ������� TCP
    public string serverIP = "localhost";
    public int serverPort = 9090;

    // ���� Gizmos
    public Color gizmoColor = Color.red;

    // ������ Gizmos
    public float gizmoSize = 0.02f;

    // ������ ��� ����������� ��������� ������������� ������
    public Text textMesh;

    private TcpClient client;
    private NetworkStream stream;
    private byte[] buffer = new byte[1024];

    void Start()
    {
        // ����������� � ������� TCP
        client = new TcpClient(serverIP, serverPort);
        stream = client.GetStream();
    }

    void Update()
    {
        // ����� ������ ����� TCP-����������
        if (stream.DataAvailable)
        {
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
            string[] coordinates = message.Split(',');
            float x = float.Parse(coordinates[0]);
            float y = float.Parse(coordinates[1]);
            float z = float.Parse(coordinates[2]);
            float visibility = float.Parse(coordinates[3]);

            // ��������� Gizmos �� ������ ���������� ��������� ������������� ������
            if (visibility > 0.5f)
            {
                Vector3 position = new Vector3(x, y, z);
                Gizmos.color = gizmoColor;
                Gizmos.DrawSphere(position, gizmoSize);

                // ����������� ��������� ������������� ������
                if (textMesh != null)
                {
                    textMesh.text = "X: " + x.ToString("F2") + "\nY: " + y.ToString("F2") + "\nZ: " + z.ToString("F2");
                }
            }
        }
    }

    void OnDrawGizmos()
    {
        // ���������� Gizmos � ������ ��������������
        if (!Application.isPlaying)
        {
            Gizmos.color = Color.clear;
            Gizmos.DrawSphere(transform.position, gizmoSize);
        }
    }

    void OnDestroy()
    {
        // �������� TCP-����������
        stream.Close();
        client.Close();
    }
}
