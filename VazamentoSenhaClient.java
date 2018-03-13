package ErrorExamples;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.util.Scanner;
public class VazamentoSenhaClient {
	public static void main(String[] args) {
				try {
					Socket clientSocket = new Socket("localhost",8666); 
					DataOutputStream outputClient = new DataOutputStream(clientSocket.getOutputStream());
					System.out.println("Username: ");
					Scanner leitura = new Scanner(System.in);
					//cliente entra com username
					String username = leitura.nextLine();
					//envia a entrada para o Server
					outputClient.writeUTF(username);
					DataOutputStream outputSenhaClient = new DataOutputStream(clientSocket.getOutputStream());
					System.out.println("Senha: ");
					Scanner leituraSenha = new Scanner(System.in);
					//cliente entra com a senha
					String senha  =  leituraSenha.nextLine();
					//envia senha para o server
					outputSenhaClient.writeUTF(senha);
					//reposta Server usuario
					DataInputStream inputClient = new DataInputStream(clientSocket.getInputStream());
					String input_1 = (String) inputClient.readUTF();
					System.out.println(input_1);
					//recebe dos dados do Server senha
					DataInputStream inputClientAgain = new DataInputStream(clientSocket.getInputStream());
					//converte os dados em String
					String input_2 = (String) inputClientAgain.readUTF();
					System.out.println(input_2);	
					inputClient.close();
					leitura.close();
					inputClientAgain.close();
					leituraSenha.close();			
					clientSocket.close();
				}
				catch (Exception e) {
					System.err.println(e);
				}
	}
}
