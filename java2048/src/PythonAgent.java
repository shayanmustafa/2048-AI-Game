import java.time.Duration;
import java.util.List;
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import put.game2048.*;
import org.json.*;

// Build with: javac -cp "lib/\*" src/PythonAgent.java

public class PythonAgent implements Agent {
	HttpClient client = HttpClient.newBuilder()
		.version(HttpClient.Version.HTTP_2)
		.build();
	URI uri = URI.create("http://127.0.0.1:2048/action");

	public String stateToJSON(Board board, List<Action> possibleActions) {
		int[][] boardState = board.get();
		boolean[] allowedActions = { false, false, false, false };
		for (Action action : possibleActions) {
			int id = action.ordinal();
			allowedActions[id] = true;
		}

		JSONObject jsonObj = new JSONObject().put("board", boardState).put("actions", allowedActions);

		return jsonObj.toString();
	}

	public Action chooseAction(Board board, List<Action> possibleActions, Duration timeLimit) {
		
		String jsonString = stateToJSON(board, possibleActions);

		HttpRequest request = HttpRequest.newBuilder().uri(uri).header("Content-Type", "application/json")
				// .header("Accept", "application/json")
				.POST(BodyPublishers.ofString(jsonString)).build();

		int chosenAction;

		try {
			HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
			String responseBody = response.body();
			chosenAction = Integer.parseInt(responseBody);
		} catch (Exception e) {
			// Print exception then just pick randomly
			e.getMessage();
			chosenAction = possibleActions.get(0).ordinal();
		}

		return Action.values()[chosenAction];
	}
}