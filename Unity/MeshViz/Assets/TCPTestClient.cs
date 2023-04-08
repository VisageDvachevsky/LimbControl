using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using System.Diagnostics;

public struct LandmarkInfo
{
	public Vector3 Position;
	public float Visibility;
}

struct ServerData
{
	public float[] data;

	public LandmarkInfo[] ParseLandmarks()
    {
		if (data.Length % 3 != 0) throw new InvalidOperationException("Invalid server data!");
		LandmarkInfo[] info = new LandmarkInfo[data.Length / 3];
		for (int i = 0; i < data.Length; i+=3)
        {
			info[i / 3].Position = new Vector3(data[i], data[i + 1], data[i + 2]);
        }

		return info;
    }
}


public class TCPTestClient : MonoBehaviour {
    private const string Hostname = "localhost";
    private const int Port = 9090;

    #region private members 	
    private TcpClient socketConnection; 	
	private Thread clientReceiveThread;
	private bool isWorking = false;

	private bool dataHandled = true;
	private ServerData serverData;

	#endregion

	public LandmarkInfo[] Landmarks;

	private Thread pythonThread;

	void Start () {
		pythonThread = new Thread(StartPythonScript);
		pythonThread.Start();
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

    private void OnApplicationQuit()
    {
        pythonThread.Abort();
    }

    private void StartPythonScript()
	{
		ProcessStartInfo startInfo = new ProcessStartInfo();
		startInfo.FileName = "python";
		startInfo.Arguments = @"C:\Users\Ya\Documents\GitHub\My-Just-Dance\Python\Main.py";
		startInfo.UseShellExecute = false;
		startInfo.RedirectStandardOutput = true;
		Process process = new Process();
		process.StartInfo = startInfo;
		process.Start();
		string output = process.StandardOutput.ReadToEnd();
		process.WaitForExit();
	}
}