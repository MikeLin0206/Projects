module Tetris_game(CLK,Turn,Down,Left,Right,current,COL,EN,DATA_R,DATA_G,DATA_B);
    output reg [7:0] DATA_R,DATA_G,DATA_B;
	 output reg [2:0] COL;
	 output reg [5:0]current;
	 output reg EN;
	 input CLK,Turn,Down,Left,Right;
	 reg right,left,turn,down;
	 reg [2:0] factor;
	 reg permit,re;
	 reg [3:0] mode1;
	 reg [7:0] plate [7:0];
	 reg [7:0] store [7:0];
	 reg [5:0] random2,random1,diff1,diff2,diff3;
	 integer i,j,k,m,point;
	 
	 divfreq F0(CLK,CLK_div);
	 divfreq1 F1(CLK,re,CLK_div2);
	 divfreq2 F2(CLK,CLK_div1);
	 byte count,run;
	 
	 initial
	   begin
	     plate[0] = 8'b11111111;
		  plate[1] = 8'b11111111;
		  plate[2] = 8'b11111111;
		  plate[3] = 8'b11111111;
		  plate[4] = 8'b11111111;
		  plate[5] = 8'b11111111;
		  plate[6] = 8'b11111111;
		  plate[7] = 8'b11111111;
		  DATA_G = 8'b11111111;
	     DATA_B = 8'b11111111;
		  current = 3;
	     factor = 1;
	     run = 0;
	     mode1 = 2;
        count = 0;
		  permit = 0;
		  random1 = 546;
		  random2 = 18;
		  right = 0;
		  left = 0;
		  turn = 0;
		  re = 0;
	   end
	 
	 always@(posedge CLK_div)
	   begin
	     if(count >= 7)
	 	    count <= 0;
		  else
			 count <= count + 1;
	     COL = count;
		  EN = 1'b1;
		  DATA_R <= plate[count];
	    end

	  
	 always@(posedge CLK_div1)
	   begin
	     random1 = (6 * (random1*(run+6)) + 7) % 34;
		  random2 = (random1 % 12) + 1;
		  
		  if((random2 == 7))
		    random2 = random2 +2;
		  else if(random2 == 8)
		    random2 = random2 +2;
		  
		  right = Right;
		  left = Left;
		  turn = Turn;
		  down = Down;
		  
	     //Store the default matrix 
	     if((run == 0) && (permit == 0))
		    begin
			 diff1 = 0;
			 diff2 = 0;
			 diff3 = 0;
			 for(j = 0;j < 8;j = j + 1)
			   begin
				  point = 0;
				  for(k = 0;k < 8;k = k + 1)    
				    begin
					   if(plate[k][j] == 1'b0)
						    point = point + 1;
				    end
			     if(point == 8)
			       begin
			         for(k = 0;k <8;k = k + 1)
			           begin
						    for(m = j;m > 0;m = m - 1)
							   begin 
					           plate[k][m] = plate[k][m - 1];
								end 
							  plate[k][0] = 1'b1;	
					     end
				    end
		      end
			 current = 3;
			 factor = 1;
			 for(k = 0;k < 8;k = k + 1)
			   begin
				  store[k] = plate[k];
				end
			 for(i = 0;i < 8;i = i + 1)
			   begin
				  if(plate[i][0] == 1'b0)
				    begin
				      mode1 = 0;
						break;
				    end
				end	 
			 end

		  // mode1 1 for square   O
		  //                      OO
		  //                      O
        if(mode1 == 1)
		    begin
		    if(CLK_div2 == 1)    //square starts falling    
		      begin
              if(run == 0 || run == 1)
				    begin
		              if((plate[current][run+2] == 1'b0) || (plate[current+1][run+1] == 1'b0))  
				          begin
							   if(run == 0)                  
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 7;
					         plate[current+1] = plate[current +1] - 2;
								run = run + 1;
								permit = 0;
							 end
					 end	  
				  else 
				    begin
					   if((plate[current][run+2] == 1'b0) || (plate[current+1][run+1] == 1'b0))
						  begin
						    run = 0;
							 mode1 = random2;
						  end
						else
						  begin
				          plate[current] = plate[current] - 7*(2**(factor));
				     	    plate[current + 1] = plate[current + 1] - 2*(2**(factor));
					       factor = factor + 1;
							 run = run + 1;
						  end
			       end  
		        if(run == 6)    //another square starts falling with most rows
				    begin
				      run = 0;
				      mode1 = random2;
				    end
			   end
				if((turn == 1) && (current != 0))
				    begin
                  mode1 = 2;
                  plate[current-1][run] = 1'b0;
					   plate[current][run-1] = 1'b1;
						current = current - 1;
						run = run + 1;
						if(run > 2)
						  factor = factor + 1;
               end 
		    end
			
		  
	     // mode1 2 for square   OOO
		  //                       O
        else if(mode1 == 2)	 
		    begin
		      if(CLK_div2 == 1)    //square starts falling    
		        begin
                if(run == 0 || run == 1)
					   begin
		              if((plate[current][run] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
							       run = 0;	  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 1;
					         plate[current+1] = plate[current +1] - 3;
								plate[current+2] = plate[current +2] - 1;
								run = run + 1;
								permit = 0;
							 end
					   end	  
				    else 
				      begin
					     if((plate[current][run] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run] == 1'b0))
						    begin
						      run = 0;
							   mode1 = random2;
						    end
						  else
						    begin
				            plate[current] = plate[current] - 1*(2**(factor));
				     	      plate[current + 1] = plate[current + 1] - 3*(2**(factor));
								plate[current + 2] = plate[current + 2] - 1*(2**(factor));
					         factor = factor + 1;
							   run = run + 1;
						    end
				      end
				    if(run == 7)    //another square starts falling with most rows
				      begin
				        run = 0;
				        mode1 = random2;
				      end
				  end
			     if(turn == 1)
				    begin
                  mode1 = 3;
                  plate[current][run] = 1'b0;
                  plate[current][run-1] = 1'b1;
						plate[current+1][run+1] = 1'b0;
						plate[current+2][run-1] = 1'b1;
                end	  
			   end		  
		  // mode1 3 for square    O
		  //                      OO
		  //                       O
		    
	     else if(mode1 == 3)
		    begin
		    if(CLK_div2 == 1)    //square starts falling    
		      begin
              if(run == 0 || run == 1)
				    begin
		              if((plate[current][run+1] == 1'b0) || (plate[current+1][run+2] == 1'b0))
				          begin
				           	if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 2;
					         plate[current+1] = plate[current +1] - 7;
								run = run + 1;
								permit = 0;
							 end
					 end	  
				  else 
				    begin
					   if((plate[current][run+1] == 1'b0) || (plate[current+1][run+2] == 1'b0))
						  begin
						    run = 0;
							 mode1 = random2;
						  end
						else
						  begin
				          plate[current] = plate[current] - 2*(2**(factor));
				     	    plate[current + 1] = plate[current + 1] - 7*(2**(factor));
					       factor = factor + 1;
							 run = run + 1;
						  end
				    end  
		        if(run == 6)    //another square starts falling with most rows
				    begin
				      run = 0;
				      mode1 = random2;
				    end
				end
				if((turn == 1) && (current != 6))
				    begin
                  mode1 = 4;
                  plate[current+2][run] = 1'b0;
                  plate[current+1][run+1] = 1'b1;
                end
			end
			  
	     // mode1 4 for square    O
		  //                      OOO
        else if(mode1 == 4)  	 
		    begin
		      if(CLK_div2 == 1)    //square starts falling    
		        begin
                if(run == 0 || run == 1)
					   begin
		              if((plate[current][run+1] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run+1] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 2;
					         plate[current+1] = plate[current +1] - 3;
								plate[current+2] = plate[current +2] - 2;
								run = run + 1;
								permit = 0;
							 end
					   end	  
				    else 
				      begin
					     if((plate[current][run+1] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run+1] == 1'b0))
						    begin
						      run = 0;
							   mode1 = random2;
						    end
						  else
						    begin
				            plate[current] = plate[current] - 2*(2**(factor));
				     	      plate[current + 1] = plate[current + 1] - 3*(2**(factor));
								plate[current + 2] = plate[current + 2] - 2*(2**(factor));
					         factor = factor + 1;
							   run = run + 1;
						    end
				      end
				    if(run == 7)    //another square starts falling with most rows
				      begin
				        run = 0;
				        mode1 = random2;
				      end
				  end
				  if(turn == 1)
				    begin
                  mode1 = 1;
                  plate[current+1][run+1] = 1'b0;
                  plate[current][run] = 1'b1;
						current = current + 1;
                end
				 end			 
	     // mode1 5 for square    OO
		  //                      OO
        else if(mode1 == 5)  	 
		    begin
		      if(CLK_div2 == 1)    //square starts falling    
		        begin
                if(run == 0 || run == 1)
					   begin
		              if((plate[current][run+1] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 2;
					         plate[current+1] = plate[current +1] - 3;
								plate[current+2] = plate[current +2] - 1;
								run = run + 1;
								permit = 0;
							 end
					   end	  
				    else 
				      begin
					     if((plate[current][run+1] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run] == 1'b0))
						    begin
						      run = 0;
							   mode1 = random2;
						    end
						  else
						    begin
				            plate[current] = plate[current] - 2*(2**(factor));
				     	      plate[current + 1] = plate[current + 1] - 3*(2**(factor));
								plate[current + 2] = plate[current + 2] - 1*(2**(factor));
					         factor = factor + 1;
							   run = run + 1;
						    end
				       end
				    if(run == 7)    //another square starts falling with most rows
				      begin
				        run = 0;
				        mode1 = random2;
				      end
				    end
					 if(turn == 1)
				    begin
                  mode1 = 6;
                  plate[current+2][run] = 1'b0;;
                  plate[current][run] = 1'b1;
						plate[current+2][run+1] = 1'b0;
						plate[current+2][run-1] = 1'b1;
						current = current + 1;
               end
				 end
				  
			  
		  // mode1 6 for square   O
		  //                      OO
		  //                       O
		    
	     else if(mode1 == 6)
		    begin
		    if(CLK_div2 == 1)    //square starts falling    
		      begin
              if(run == 0 || run == 1)
				    begin
		              if((plate[current][run+1] == 1'b0) || (plate[current+1][run+2] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 3;
					         plate[current+1] = plate[current +1] - 6;
								run = run + 1;
								permit = 0;
							 end
					 end	  
				  else 
				    begin
					   if((plate[current][run+1] == 1'b0) || (plate[current+1][run+2] == 1'b0))
						  begin
						    run = 0;
							 mode1 = random2;
						  end
						else
						  begin
				          plate[current] = plate[current] - 3*(2**(factor));
				     	    plate[current + 1] = plate[current + 1] - 6*(2**(factor));
					       factor = factor + 1;
							 run = run + 1;
						  end
				    end  
		        if(run == 6)    //another square starts falling with most rows
				    begin
				      run = 0;
				      mode1 = random2;
				    end
				end
				if((turn == 1))
				    begin
                  mode1 = 5;
                  plate[current+1][run-1] = 1'b0;
                  plate[current][run-1] = 1'b1;
						plate[current+2][run-1] = 1'b0;
                  plate[current+1][run+1] = 1'b1;
                end
			end

        // mode1 9 for square   O
		  //                      OOO
		  else if(mode1 == 9)  	 
		    begin
		      if(CLK_div2 == 1)    //square starts falling    
		        begin
                if(run == 0 || run == 1)
					   begin
		              if((plate[current][run+1] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run+1] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 3;
					         plate[current+1] = plate[current +1] - 2;
								plate[current+2] = plate[current +2] - 2;
								run = run + 1;
								permit = 0;
							 end
					   end	  
				    else 
				      begin
					     if((plate[current][run+1] == 1'b0) || (plate[current+1][run+1] == 1'b0) ||
						     (plate[current+2][run+1] == 1'b0))
						    begin
						      run = 0;
							   mode1 = random2;
						    end
						  else
						    begin
				            plate[current] = plate[current] - 3*(2**(factor));
				     	      plate[current + 1] = plate[current + 1] - 2*(2**(factor));
								plate[current + 2] = plate[current + 2] - 2*(2**(factor));
					         factor = factor + 1;
							   run = run + 1;
						    end
				      end
				    if(run == 7)    //another square starts falling with most rows
				      begin
				        run = 0;
				        mode1 = random2;
				      end
				    end
					 if(turn == 1)
				    begin
                  mode1 = 10;
                  plate[current][run+1] = 1'b0;
                  plate[current+1][run] = 1'b1;
						plate[current+1][run-1] = 1'b0;
						plate[current+2][run] = 1'b1;
                end
			 end

		  // mode1 10 for square  OO
		  //                      O
		  //                      O
		    
	     else if(mode1 == 10)
		    begin
		    if(CLK_div2 == 1)    //square starts falling    
		      begin
              if(run == 0 || run == 1)
				    begin
		              if((plate[current][run+2] == 1'b0) || (plate[current+1][run] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 7;
					         plate[current+1] = plate[current +1] - 1;
								run = run + 1;
								permit = 0;
							 end
					 end	  
				  else 
				    begin
					   if((plate[current][run+2] == 1'b0) || (plate[current+1][run] == 1'b0))
						  begin
						    run = 0;
							 mode1 = random2;
						  end
						else
						  begin
				          plate[current] = plate[current] - 7*(2**(factor));
				     	    plate[current + 1] = plate[current + 1] - 1*(2**(factor));
					       factor = factor + 1;
							 run = run + 1;
						  end
				    end  
		        if(run == 6)    //another square starts falling with most rows
				    begin
				      run = 0;
				      mode1 = random2;
				    end
				  end
				  if((turn == 1) && (current != 0))
				    begin
                  mode1 = 11;
                  plate[current+1][run] = 1'b0;
                  plate[current][run] = 1'b1;
						plate[current-1][run-1] = 1'b0;
						plate[current][run+1] = 1'b1;
						current = current - 1;
                end
			  end
		
				
        // mode1 11 for square  OOO
		  //                        O
		  else if(mode1 == 11)  	 
		    begin
		      if(CLK_div2 == 1)    //square starts falling    
		        begin
                if(run == 0 || run == 1)
					   begin
		              if((plate[current][run] == 1'b0) || (plate[current+1][run] == 1'b0) ||
						     (plate[current+2][run+1] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 1;
					         plate[current+1] = plate[current +1] - 1;
								plate[current+2] = plate[current +2] - 3;
								run = run + 1;
								permit = 0;
							 end
					   end	  
				    else 
				      begin
					     if((plate[current][run] == 1'b0) || (plate[current+1][run] == 1'b0) ||
						     (plate[current+2][run+1] == 1'b0))
						    begin
						      run = 0;
							   mode1 = random2;
						    end
						  else
						    begin
				            plate[current] = plate[current] - 1*(2**(factor));
				     	      plate[current + 1] = plate[current + 1] - 1*(2**(factor));
								plate[current + 2] = plate[current + 2] - 3*(2**(factor));
					         factor = factor + 1;
							   run = run + 1;
						    end
				      end
				    if(run == 7)    //another square starts falling with most rows
				      begin
				        run = 0;
				        mode1 = random2;
				      end
				    end
					 if(turn == 1)
				    begin
                 mode1 = 12;
                 plate[current+2][run+1] = 1'b0;
                 plate[current+1][run-1] = 1'b1;
					  plate[current+1][run+1] = 1'b0;
					  plate[current][run-1] = 1'b1;
					  current = current + 1;
                end
				 end

			
		  // mode1 12 for square   O
		  //                       O
		  //                      OO
		    
	     else if(mode1 == 12)
		    begin
		    if(CLK_div2 == 1)    //square starts falling    
		      begin
              if(run == 0 || run == 1)
				    begin
		              if((plate[current][run+2] == 1'b0) || (plate[current+1][run+2] == 1'b0))
				          begin
				            if(run == 0)
								  begin
									 current = current + 1;
								    permit = 1;
								  end
								else
						        begin
								    run = 0;  
				                mode1 = random2;
									 permit = 0;
								  end
				          end
				        else		
						    begin  
				            plate[current] = plate[current] - 4;
					         plate[current+1] = plate[current +1] - 7;
								run = run + 1;
								permit = 0;
							 end
					 end	  
				  else 
				    begin
					   if((plate[current][run+2] == 1'b0) || (plate[current+1][run+2] == 1'b0))
						  begin
						    run = 0;
							 mode1 = random2;
						  end
						else
						  begin
				          plate[current] = plate[current] - 4*(2**(factor));
				     	    plate[current + 1] = plate[current + 1] - 7*(2**(factor));
					       factor = factor + 1;
							 run = run + 1;
						  end
				    end  
		        if(run == 6)    //another square starts falling with most rows
				    begin
				      run = 0;
				      mode1 = random2;
				    end
				  end
			  if((turn == 1))
				    begin
                  mode1 = 9;
                  plate[current][run-1] = 1'b0;
                  plate[current][run+1] = 1'b1;
						plate[current][run] = 1'b0;
						plate[current+1][run+1] = 1'b1;
						plate[current+2][run] = 1'b0;
						plate[current+1][run-1] = 1'b1;
                end
				end
			 
		  diff1 = store[current] - plate[current];
		  diff2 = store[current + 1] - plate[current + 1];
		  diff3 = store[current + 2] - plate[current + 2];
			  				
			if(right == 1)
          begin
			   if((((mode1 == 8) || (mode1 == 10))                  && (plate[current+2][run-1] != 1'b0) && (plate[current+2][run] != 1'b0) && (plate[current+1][run+1] != 1'b0)) ||
				   (((mode1 == 3) || (mode1 == 12) || (mode1 == 16)) && (plate[current+2][run-1] != 1'b0) && (plate[current+2][run] != 1'b0) && (plate[current+2][run+1] != 1'b0)) ||
				   ((mode1 == 1)  && (plate[current+1][run-1] != 1'b0) && (plate[current+2][run] != 1'b0) && (plate[current+1][run+1] != 1'b0)) ||
			      ((mode1 == 6)  && (plate[current+1][run-1] != 1'b0) && (plate[current+2][run] != 1'b0) && (plate[current+2][run+1] != 1'b0)) ||
				   ((mode1 == 14) && (plate[current+1][run-1] != 1'b0) && (plate[current+1][run] != 1'b0) && (plate[current+2][run+1] != 1'b0)) ||
					((mode1 == 17) && (plate[current+2][run-1] != 1'b0) && (plate[current+2][run] != 1'b0) && (current+1 < 7)) )
				  begin
		          plate[current+2] = store[current+2] - diff2;
					 plate[current+1] = store[current+1] - diff1;
					 plate[current] = store[current];
					 current = current + 1;
//					 diff1 = store[current] - plate[current];
//		          diff2 = store[current + 1] - plate[current + 1];
//					 diff3 = store[current + 2] - plate[current + 2];
		        end
		      else if((((mode1 == 2)  || (mode1 == 5))  && (plate[current+3][run-1] != 1'b0) && (plate[current+2][run] != 1'b0))  ||
				        (((mode1 == 11) || (mode1 == 13)) && (plate[current+3][run-1] != 1'b0) && (plate[current+3][run] != 1'b0))  ||
						  (((mode1 == 4)  || (mode1 == 7))  && (plate[current+2][run-1] != 1'b0) && (plate[current+3][run] != 1'b0))  ||
						  ((mode1 == 9)  && (plate[current+1][run-1] != 1'b0) && (plate[current+3][run] != 1'b0) && (current < 5))   ||
						  ((mode1 == 16) && (plate[current+3][run-1] != 1'b0) && (plate[current+1][run] != 1'b0) && ((current+2) < 7)))		  
              begin
				    plate[current+3] = store[current+3] - diff3;
				    plate[current+2] = store[current+2] - diff2;
					 plate[current+1] = store[current+1] - diff1;
					 plate[current] = store[current];
					 current = current + 1;
//					 diff1 = store[current] - plate[current];
//		          diff2 = store[current + 1] - plate[current + 1];
//		          diff3 = store[current + 2] - plate[current + 2];
		        end
			   else if((mode1 == 18) && (plate[current+4][run-1] != 1'b0) && ((current+3) < 7))
	           begin
			       plate[current+4] = store[current+4] - diff3;
	             plate[current] = store[current];
	             current = current + 1;
//					 diff1 = store[current] - plate[current];
	           end
		      else if((mode1 == 19) && (plate[current+1][run-1] != 1'b0)&& (plate[current+1][run] != 1'b0)&& (plate[current+1][run+1] != 1'b0)&& (plate[current+1][run+2] != 1'b0) && (current != 7))		  
              begin
				   plate[current+1] = store[current+1] - diff1;
	            plate[current] = store[current];
	            current = current + 1; 
//					diff1 = store[current] - plate[current];
				  end
			 end	
         else if((left == 1) && (current != 0))
          begin
			   if(((mode1 == 16) && (plate[current-1][run-1] != 1'b0) && (plate[current][run] != 1'b0)&& (plate[current][run+1] != 1'b0)) ||
				   (((mode1 == 1) || (mode1 == 6) || (mode1 == 10)|| (mode1 == 14)) && (plate[current-1][run-1] != 1'b0) && (plate[current-1][run] != 1'b0) && (plate[current-1][run+1] != 1'b0)) ||
				   ((mode1 == 3)  && (plate[current][run-1] != 1'b0) && (plate[current-1][run] != 1'b0) && (plate[current][run+1] != 1'b0)) ||
			      ((mode1 == 8)  && (plate[current][run-1] != 1'b0) && (plate[current-1][run] != 1'b0) && (plate[current-1][run+1] != 1'b0)) ||
				   ((mode1 == 12) && (plate[current][run-1] != 1'b0) && (plate[current][run] != 1'b0)   && (plate[current-1][run+1] != 1'b0)) ||
					((mode1 == 17) && (plate[current-1][run-1] != 1'b0) && (plate[current-1][run] != 1'b0)))
				  begin
		          plate[current-1] = store[current-1] - diff1;
					 plate[current] = store[current] - diff2;
					 plate[current+1] = store[current+1];
					 current = current - 1;
//					 diff1 = store[current] - plate[current];
//		          diff2 = store[current + 1] - plate[current + 1];
//		          diff3 = store[current + 2] - plate[current + 2];
		        end
		      else if((((mode1 == 4)  || (mode1 == 5))  && (plate[current][run-1] != 1'b0) && (plate[current-1][run] != 1'b0))    ||
				        (((mode1 == 2)  || (mode1 == 7))  && (plate[current-1][run-1] != 1'b0) && (plate[current][run] != 1'b0))    ||
						  (((mode1 == 9)  || (mode1 == 15)) && (plate[current-1][run-1] != 1'b0) && (plate[current-1][run] != 1'b0))  ||
						  ((mode1 == 11)  && (plate[current-1][run-1] != 1'b0) && (plate[current+1][run] != 1'b0))                     ||
						  ((mode1 == 13)  && (plate[current+1][run-1] != 1'b0) && (plate[current-1][run] != 1'b0)))		  
              begin
				    plate[current-1] = store[current-1] - diff1;
				    plate[current] = store[current] - diff2;
					 plate[current+1] = store[current+1] - diff3;
					 plate[current+2] = store[current+2];
					 current = current - 1;
//					 diff1 = store[current] - plate[current];
//		          diff2 = store[current + 1] - plate[current + 1];
//		          diff3 = store[current + 2] - plate[current + 2];
		        end
			   else if((mode1 == 18) && (plate[current-1][run-1] != 1'b0))
	           begin
			       plate[current-1] = store[current-1] - diff1;
	             plate[current+3] = store[current+3];
	             current = current - 1;
//					 diff1 = store[current] - plate[current];
	           end
		      else if((mode1 == 19)&& (plate[current-1][run-1] != 1'b0)&& (plate[current-1][run] != 1'b0)&& (plate[current-1][run+1] != 1'b0)&& (plate[current-1][run+2] != 1'b0))		  
              begin
				   plate[current-1] = store[current-1] - diff1;
	            plate[current] = store[current];
	            current = current - 1;
//				   diff1 = store[current] - plate[current];
//		         diff2 = store[current + 1] - plate[current + 1];
				  end
		    end

	 end
endmodule



module divfreq(input CLK, output reg CLK_div);
  reg [24:0] Count;
  always @(posedge CLK)
    begin
      if(Count > 50000)
        begin
          Count <= 25'b0;
          CLK_div <= ~CLK_div;
        end
      else
        Count <= Count + 1'b1;
    end
endmodule



module divfreq2(input CLK, output reg CLK_div1);
  reg [25:0] Count;
  always @(posedge CLK)
    begin
      if(Count > 15000000)
        begin
          Count <= 25'b0;
          CLK_div1 <= ~CLK_div1;
        end
      else
        Count <= Count + 1'b1;
    end
endmodule



module divfreq1(input CLK,re, output reg CLK_div2);
  reg [25:0] Count;
  initial
    begin
	   CLK_div2 = 0;
	 end
	 
  always @(posedge CLK)
    begin
      if(Count > 30000000)
        begin
          Count <= 25'b0;
          CLK_div2 <= ~CLK_div2;
        end
      else
        Count <= Count + 1'b1;
    end
endmodule
