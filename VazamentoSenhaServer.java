package ErrorExamples;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
public class VazamentoSenhaServer {
	public static void main(String[] args) {
		try{  
			ServerSocket sSocket=new ServerSocket(8666);  
			Socket nSocket=sSocket.accept();//establishes connection  			
			//recebe dado de usuário
			DataInputStream dataInput=new DataInputStream(nSocket.getInputStream()); 
			String entrada=(String)dataInput.readUTF();
			//exibe o usuário
			//responde a entrada do client
			DataOutputStream responseServer = new DataOutputStream(nSocket.getOutputStream());
			responseServer.writeUTF("Novo usuario: " + entrada);		
			//recebe a senha do usuario
			DataInputStream senhaInput = new DataInputStream(nSocket.getInputStream());
			//exibe a senha
			String senha = (String) senhaInput.readUTF();
			//responde a entrada do client
			DataOutputStream responseServerAgain = new DataOutputStream(nSocket.getOutputStream());	
			System.out.println("Usuario: " + entrada);
			System.out.println("Senha: " + senha);//erro
			responseServerAgain.writeUTF("ERRO, senha : " + senha + "EXIBIDA NA TELA");			
			sSocket.close();
		}
		catch(Exception e){
			System.out.println(e);
		} 
	}
}
