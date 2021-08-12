import java.time.Duration;
import java.util.List;
import put.game2048.*;

public class TestApp {
    public static void main(String[] args) throws Exception {
		Agent agent = new PythonAgent();
		
		int[][] testState = {
			{0,1,2,3},
			{4,5,6,7},
			{8,9,10,11},
			{12,13,14,15}
		};
		Board testBoard = new Board(testState);
		List<Action> testActions = List.of(Action.DOWN);
		Duration duration = Duration.ofMillis(1);

		Action action = agent.chooseAction(testBoard, testActions, duration);

		System.out.println(action);
    }
}
