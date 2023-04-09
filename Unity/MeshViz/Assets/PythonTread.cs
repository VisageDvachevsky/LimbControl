using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using UnityEngine;

public class PythonTread : MonoBehaviour
{
    private Thread pythonThread;

    private void Start()
    {
    }

	private void OnApplicationQuit()
	{
		pythonThread.Abort();
	}

	private void StartPythonScript()
	{
		using Process process = Process.Start(new ProcessStartInfo
		{
			FileName = "python",
			Arguments = @"C:\Users\Ya\Desktop\ûûûû\main.py",
			UseShellExecute = false,
			RedirectStandardInput = true,
			RedirectStandardOutput = true
		});
	}
}
