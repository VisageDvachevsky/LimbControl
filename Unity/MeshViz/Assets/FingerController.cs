using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;
using System.Text;

public class FingerController : MonoBehaviour
{
    // адрес и порт сервера TCP
    public string serverIP = "localhost";
    public int serverPort = 9090;

    // цвет Gizmos
    public Color gizmoColor = Color.red;

    // размер Gizmos
    public float gizmoSize = 0.02f;

    // скрипт дл€ отображени€ координат указательного пальца
    public Text textMesh;

    private TcpClient client;
    private NetworkStream stream;
    private byte[] buffer = new byte[1024];

    void Start()
    {
        // подключение к серверу TCP
        client = new TcpClient(serverIP, serverPort);
        stream = client.GetStream();
    }

    void Update()
    {
        // прием данных через TCP-соединение
        if (stream.DataAvailable)
        {
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
            string[] coordinates = message.Split(',');
            float x = float.Parse(coordinates[0]);
            float y = float.Parse(coordinates[1]);
            float z = float.Parse(coordinates[2]);
            float visibility = float.Parse(coordinates[3]);

            // рисование Gizmos на основе полученных координат указательного пальца
            if (visibility > 0.5f)
            {
                Vector3 position = new Vector3(x, y, z);
                Gizmos.color = gizmoColor;
                Gizmos.DrawSphere(position, gizmoSize);

                // отображение координат указательного пальца
                if (textMesh != null)
                {
                    textMesh.text = "X: " + x.ToString("F2") + "\nY: " + y.ToString("F2") + "\nZ: " + z.ToString("F2");
                }
            }
        }
    }

    void OnDrawGizmos()
    {
        // отключение Gizmos в режиме редактировани€
        if (!Application.isPlaying)
        {
            Gizmos.color = Color.clear;
            Gizmos.DrawSphere(transform.position, gizmoSize);
        }
    }

    void OnDestroy()
    {
        // закрытие TCP-соединени€
        stream.Close();
        client.Close();
    }
}
