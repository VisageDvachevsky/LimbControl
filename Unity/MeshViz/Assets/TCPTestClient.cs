using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using System.Diagnostics;
using Newtonsoft.Json;

public struct ServerChunk {
	public float x;
	public float y;
	public float z;
	public int point;
}

struct ServerData
{
	public float[] data;

	public ServerChunk[] ParseLandmarks()
    {
		if (data.Length % 4 != 0) throw new InvalidOperationException("Invalid server data!");
		ServerChunk[] info = new ServerChunk[data.Length / 4];
		for (int i = 0; i < data.Length; i+=4)
        {
			info[i / 4].x = data[i];
			info[i / 4].y = data[i + 1];
			info[i / 4].z = data[i + 2];
			info[i / 4].point = ((int)data[i + 3]);

		}

		return info;
    }
}


public class TCPTestClient : MonoBehaviour {
    private const string Hostname = "localhost";
    private const int Port = 9090;
    private const string V = @"C:\Users\Ya\AppData\Local\Programs\Python\Python310\python.exe";

    #region private members 	
    private TcpClient socketConnection; 	
	private Thread clientReceiveThread;
	private bool isWorking = false;

	private bool dataHandled = true;
	private ServerData serverData;

	#endregion

	public ServerChunk[] Landmarks;

	

	void Start () {
		ProcessStartInfo startInfo = new ProcessStartInfo();
        startInfo.FileName = V;
		startInfo.Arguments = @"cd C:\Users\Ya\Desktop\ûûûû\python3 main.py";
		startInfo.UseShellExecute = false;

		Process process = new Process();
		process.StartInfo = startInfo;
		process.Start();
        process.WaitForExit();


		ConnectToTcpServer();     
	}  	

	void Update () {
		if (!dataHandled)
        {
			Landmarks = serverData.ParseLandmarks();
			dataHandled = true;
        }
	}

    private void OnDestroy()
    {
		isWorking = false;
    }

    private void ConnectToTcpServer () {

        Thread.Sleep(20000);
		print("123");


		try {  			
			clientReceiveThread = new Thread (new ThreadStart(ListenForData)); 
			clientReceiveThread.IsBackground = true;
			isWorking = true;
			clientReceiveThread.Start();  		
		} 		
		catch (Exception e) {
            UnityEngine.Debug.Log("On client connect exception " + e); 		
		} 	
	}  	
	/// <summary> 	
	/// Runs in background clientReceiveThread; Listens for incomming data. 	
	/// </summary>     
	private void ListenForData() { 		
		try { 			
			socketConnection = new TcpClient(Hostname, Port);  			
			Byte[] bytes = new Byte[4096];             
			while (isWorking) { 				
				// Get a stream object for reading 				
				using (NetworkStream stream = socketConnection.GetStream()) { 					
					int length; 					
					// Read incomming stream into byte arrary. 					
					while ((length = stream.Read(bytes, 0, bytes.Length)) != 0) { 						
						var incommingData = new byte[length]; 						
						Array.Copy(bytes, 0, incommingData, 0, length); 						
						// Convert byte array to string message. 						
						string serverMessage = Encoding.ASCII.GetString(incommingData);
						if (serverMessage[0] == '{' && serverMessage[serverMessage.Length - 1] == '}')
						{
							if (dataHandled)
                            {
								ServerData data = JsonUtility.FromJson<ServerData>(serverMessage);
								serverData = data;
								dataHandled = false;
							}
						}
					} 				
				} 			
			}
			socketConnection.Close();
		}         
		catch (SocketException socketException) {
			UnityEngine.Debug.Log("Socket exception: " + socketException);         
		}     
	}  	
	/// <summary> 	
	/// Send message to server using socket connection. 	
	/// </summary> 	
	private void SendMessage() {         
		if (socketConnection == null) {             
			return;         
		}  		
		try { 			
			// Get a stream object for writing. 			
			NetworkStream stream = socketConnection.GetStream(); 			
			if (stream.CanWrite) {                 
				string clientMessage = "This is a message from one of your clients."; 				
				// Convert string message to byte array.                 
				byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage); 				
				// Write byte array to socketConnection stream.                 
				stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);
				UnityEngine.Debug.Log("Client sent his message - should be received by server");             
			}         
		} 		
		catch (SocketException socketException) {
			UnityEngine.Debug.Log("Socket exception: " + socketException);         
		}     
	}

    
}