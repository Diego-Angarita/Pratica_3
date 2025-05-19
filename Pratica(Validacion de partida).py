""" 1. d4 d5 2. Bf4 Nf6 3. e3 e6 4. c3 c5 5. Nd2 Nc6 6. Bd3 Bd6 7. Bg3 O-O 8. Ngf3 Qe7 9. Ne5
Nd7 10. Nxc6 bxc6 11. Bxd6 Qxd6 12. Nf3 a5 13. O-O Ba6 14. Re1 Rfb8 15. Rb1 Bxd3 16.
Qxd3 c4 17. Qc2 f5 18. Nd2 Rb5 19. b3 cxb3 20. axb3 Ra8 21. Qa2 Qc7 22. c4 Rb4 23. cxd5
cxd5 24. Rbc1 Qb6 25. h3 a4 26. bxa4 Rb2 27. Qa3 Rxd2 28. Qe7 Qd8 29. Qxe6+ Kh8 30.
Qxf5 Nf6 31. g4 Ne4 32. Rf1 h6 33. Rc6 Qh4 34. Rc8+ Rxc8 35. Qxc8+ Kh7 """

"""
Chess Notation Validator

This program validates chess moves based on a specific notation grammar and 
checks a list of example moves for correctness.
"""

import re

class ChessNotationValidator:
    def __init__(self):
        # Define the grammar components based on the provided specification
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.pieces = ["K", "Q", "R", "B", "N"]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
        # Compile regex patterns for different components
        self.pattern_enroque = re.compile(r"^(O-O|O-O-O)$")
        self.pattern_casilla = re.compile(r"^[a-h][1-8]$")
        self.pattern_letra = re.compile(r"^[a-h]$")
        self.pattern_numero = re.compile(r"^[1-8]$")
        self.pattern_pieza = re.compile(r"^[KQRBN]$")
        self.pattern_numero_turno = re.compile(r"^\d+$")
        self.pattern_jaque_mate = re.compile(r"^[+#]$")
        self.pattern_captura = re.compile(r"^x$")
        self.pattern_promocion = re.compile(r"^=[KQRBN]$")
        
        # Patterns for complete move types
        self.pattern_movimiento_pieza = re.compile(
            r"^([KQRBN])([a-h]|[1-8]|[a-h][1-8])?(x)?([a-h][1-8])(=[KQRBN])?([+#])?$"
        )
        self.pattern_peon_captura = re.compile(
            r"^([a-h])x([a-h][1-8])(=[KQRBN])?([+#])?$"
        )
        self.pattern_peon_avance = re.compile(
            r"^([a-h][1-8])(=[KQRBN])?([+#])?$"
        )
    
    def validate_numero_turno(self, text):
        """Validate a turn number."""
        return bool(self.pattern_numero_turno.match(text))
    
    def validate_enroque(self, text):
        """Validate castling notation."""
        return bool(self.pattern_enroque.match(text))
    
    def validate_movimiento_pieza(self, text):
        """Validate a piece movement."""
        return bool(self.pattern_movimiento_pieza.match(text))
    
    def validate_peon_captura(self, text):
        """Validate a pawn capture move."""
        return bool(self.pattern_peon_captura.match(text))
    
    def validate_peon_avance(self, text):
        """Validate a pawn advance move."""
        return bool(self.pattern_peon_avance.match(text))
    
    def validate_jugada(self, text):
        """Validate a complete move."""
        # Check if it's castling
        if self.validate_enroque(text):
            return True
        
        # Check if it's a piece movement
        if self.validate_movimiento_pieza(text):
            return True
        
        # Check if it's a pawn capture
        if self.validate_peon_captura(text):
            return True
        
        # Check if it's a pawn advance
        if self.validate_peon_avance(text):
            return True
        
        return False
    
    def validate_turn(self, turn_text):
        """Validate a complete turn (number + white move + optional black move)."""
        parts = turn_text.strip().split()
        
        # Check if we have at least a turn number and a white move
        if len(parts) < 2:
            return False, f"Turn '{turn_text}' doesn't have enough parts"
        
        # Validate turn number (should end with a dot)
        turn_num = parts[0]
        if not turn_num.endswith('.'):
            return False, f"Turn number '{turn_num}' should end with a dot"
        
        if not self.validate_numero_turno(turn_num[:-1]):
            return False, f"'{turn_num[:-1]}' is not a valid turn number"
        
        # Validate white move
        white_move = parts[1]
        if not self.validate_jugada(white_move):
            return False, f"'{white_move}' is not a valid white move"
        
        # Validate black move if present
        if len(parts) > 2:
            black_move = parts[2]
            if not self.validate_jugada(black_move):
                return False, f"'{black_move}' is not a valid black move"
        
        return True, "Valid turn"
    
    def validate_game(self, game_text):
        """Validate an entire game notation."""
        turns = game_text.strip().split('\n')
        results = []
        
        for i, turn in enumerate(turns):
            is_valid, message = self.validate_turn(turn)
            if not is_valid:
                results.append(f"Error in turn {i+1}: {message}")
        
        if not results:
            results.append("All turns are valid")
        
        return results


def parse_example_moves(example_text):
    """Parse the moves from the example image."""
    # Split by periods to separate the move numbers
    moves = []
    parts = example_text.split('.')
    
    # Skip the first empty part if it exists
    start_idx = 0
    if not parts[0].strip():
        start_idx = 1
    
    for i in range(start_idx, len(parts)):
        part = parts[i].strip()
        if not part:
            continue
            
        # Extract move number and the actual moves
        move_parts = part.split()
        
        # Handle the first part which might contain the move number
        if i > 0 and move_parts[0].isdigit():
            move_num = move_parts[0]
            actual_moves = move_parts[1:]
        else:
            move_num = str(i)
            actual_moves = move_parts
            
        # Create the formatted turn
        if actual_moves:
            turn = f"{move_num}. {' '.join(actual_moves)}"
            moves.append(turn)
    
    return moves


# Example moves from the second image
example_moves = """
1. d4 d5 2. Bf4 Nf6 3. e3 e6 4. c3 c5 5. Nd2 Nc6 6. Bd3 Bd6 7. Bg3 O-O 8. Ngf3 Qe7 9. Ne5
Nd7 10. Nxc6 bxc6 11. Bxd6 Qxd6 12. Nf3 a5 13. O-O Ba6 14. Re1 Rfb8 15. Rb1 Bxd3 16.
Qxd3 c4 17. Qc2 f5 18. Nd2 Rb5 19. b3 cxb3 20. axb3 Ra8 21. Qa2 Qc7 22. c4 Rb4 23. cxd5
cxd5 24. Rbc1 Qb6 25. h3 a4 26. bxa4 Rb2 27. Qa3 Rxd2 28. Qe7 Qd8 29. Qxe6+ Kh8 30.
Qxf5 Nf6 31. g4 Ne4 32. Rf1 h6 33. Rc6 Qh4 34. Rc8+ Rxc8 35. Qxc8+ Kh7
"""

def validate_game_text(game_text, validator):
    """Validate a game from text input."""
    # Simple parsing to extract moves better aligned with the grammar
    parsed_moves = []
    move_pattern = re.compile(r'(\d+)\.\s+(\S+)(?:\s+(\S+))?')
    
    for match in move_pattern.finditer(game_text):
        turn_num, white_move, black_move = match.groups()
        if black_move:
            parsed_moves.append(f"{turn_num}. {white_move} {black_move}")
        else:
            parsed_moves.append(f"{turn_num}. {white_move}")
    
    results = []
    # Validate each parsed move
    results.append("Validating chess moves...")
    for move in parsed_moves:
        is_valid, message = validator.validate_turn(move)
        results.append(f"{move}: {'Valid' if is_valid else 'Invalid - ' + message}")
    
    results.append("\nAnalyzing individual moves...")
    # Analyze individual moves without turn structure
    all_moves = []
    for move in game_text.split():
        if not move.endswith('.') and not move[0].isdigit() and move not in ['O-O', 'O-O-O']:
            # This appears to be an actual chess move (not a turn number)
            if validator.validate_jugada(move):
                all_moves.append((move, "Valid"))
            else:
                all_moves.append((move, "Invalid"))
    
    for move, status in all_moves:
        results.append(f"{move}: {status}")
    
    return results


def main():
    # Create the validator
    validator = ChessNotationValidator()
    
    print("Chess Notation Validator")
    print("=======================")
    print("1. Enter your own chess game")
    print("2. Exit")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == "1":
        print("\nEnter your chess game notation.")
        print("Format example: 1. e4 e5 2. Nf3 Nc6")
        print("Enter a blank line when done.")
        
        game_lines = []
        while True:
            line = input("> ")
            if line.strip() == "":
                break
            game_lines.append(line)
        
        user_game = "\n".join(game_lines)
        if not user_game.strip():
            print("No input provided.")
            return
            
        results = validate_game_text(user_game, validator)
        for result in results:
            print(result)
    
    elif choice == "2":
        print("Exiting program.")
        return
    
    else:
        print("Invalid choice. Please run the program again.")


if __name__ == "__main__":
    main()