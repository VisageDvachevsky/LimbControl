// This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. 
// To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/ 
// or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

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
		if (data.Length % 4 != 0) throw new InvalidOperationException("Invalid server data!");
		LandmarkInfo[] info = new LandmarkInfo[data.Length / 4];
		for (int i = 0; i < data.Length; i+=4)
        {
			info[i / 4].Position = new Vector3(data[i], data[i + 1], data[i + 2]);
			info[i / 4].Visibility = data[i + 3];
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

	// Use this for initialization 	
	void Start () {
		ConnectToTcpServer();     
	}  	
	// Update is called once per frame
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
    /// <summary> 	
    /// Setup socket connection. 	
    /// </summary> 	
    private void ConnectToTcpServer () { 		
		try {  			
			clientReceiveThread = new Thread (new ThreadStart(ListenForData)); 
			clientReceiveThread.IsBackground = true;
			isWorking = true;
			clientReceiveThread.Start();  		
		} 		
		catch (Exception e) { 			
			Debug.Log("On client connect exception " + e); 		
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
			Debug.Log("Socket exception: " + socketException);         
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
				Debug.Log("Client sent his message - should be received by server");             
			}         
		} 		
		catch (SocketException socketException) {             
			Debug.Log("Socket exception: " + socketException);         
		}     
	} 
}