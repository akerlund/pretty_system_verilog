/* TODO:

  Use ';' in comments

*/
/*
  Header one of module top_module #(
*/
// Header two of module top_module #(
/**
   Header three of module top_module #(
  */

  // Header four
  // of module top_module #(
/*

A parsing FSM:

1. keyword parameter
2. type
3. range, i.e., []
4. name
5. =
5.1 if not '=' illegal range, move to brackets
6. value $() OR \w \d
7.1: ',' -> key word parameter -> 2
7.2: ',' -> name (type/range the same) -> 4
7.3: );  -> exit

*/

import some_pkg::*;

import some_pkg::*;


module top_module #(
  parameter int PARAMETER0_P  = -1,
  parameter logic PARAMETER1_P  = -1, // " ' $ % ' ` + * < > | & ^ . { } # :
  parameter logic [7 : 0] [1:0] [4 :0] PARAMETER2_P  = -1, // " ' $ % ' ` + * < > | & ^ . { } # :
  parameter int PARAMETER3_P = $clog2(PARAMETER1_P)
)(
  // Clock and reset
  input  wire  clk, // clk " ' $ % ' ` + * < > | & ^ . { } # :
  input  wire                rst_n,  // rst_n
  // STANDALONE COMMENT 0
  input wire   [PARAMETER0_P-1 : 0]                          valid0, // valid0
  output logic[NR_OF_MASTERS_P-1 : 0]               ready0, /*ready0*/
  input wire   [PARAMETER0_P/*idi]ot*/-1:0] [$clog2(PARAMETER1_P / 2)-1 : 0][PARAMETER2_P-1 : 0] data0, /*data0*/
  // STANDALONE COMMENT 1
  input wire   [PARAMETER0_P-1 : 0]                          valid1, // valid1?!#
  // STANDALONE COMMENT 2
  output logic[PARAMETER0_P-1 : 0]                          ready1, // ready1
  // STANDALONE COMMENT 3
  input wire   [PARAMETER3_P-1:0] [PARAMETER4_P-1 : 0][PARAMETER5_P-1 : 0] data1 //data1

  );

parameter illegal = 666;

localparam logic [$clog2(PARAMETER0_P)-1 : 0] LOCALPARAM_C = 1;

typedef enum {
  ENUM0_E,
  ENUM1_E
} enum_t;


enum_t enum_i0;


logic [$clog2(PARAMETER0_P)-1 : 0] logic0;
logic [63 : 0] logic1;
logic logic2;
logic [63 : 0] [15 : 0] logic3;


assign logic0 = logic2;
assign logic1 = logic3;
assign logic2 = logic0;
assign logic3 = logic1;

submodule00 submodule00_i0 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);

submodule01 submodule01_i0 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);

// FSM
always_ff @(posedge clk or negedge rst_n) begin
  if ( !rst_n ) begin
    logic0 <= '0;
    logic1  <= '0;
  end
  else begin

    // Comment

    if (logic2 ) // irritating comment
    begin
      case (logic3)
        // Comment
        0:
        begin
          logic0 <= 42;
        end
        1: begin
          // Comment
        logic1 <= logic0;
          end

          default: begin// Comment
    // Comment

            logic0 <= logic0;
logic1 <= logic1;
          end
      endcase

    end
  end
end

endmodule