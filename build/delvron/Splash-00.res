tcl86t.dll      tk86t.dll       tk              __splash              �  o  �   �   Xtk\ttk\utils.tcl tk\tk.tcl tk\ttk\cursors.tcl tk\ttk\fonts.tcl VCRUNTIME140.dll tk\ttk\ttk.tcl tk86t.dll tcl86t.dll tk\license.terms tk\text.tcl proc _ipc_server {channel clientaddr clientport} {
set client_name [format <%s:%d> $clientaddr $clientport]
chan configure $channel \
-buffering none \
-encoding utf-8 \
-eofchar \x04 \
-translation cr
chan event $channel readable [list _ipc_caller $channel $client_name]
}
proc _ipc_caller {channel client_name} {
chan gets $channel cmd
if {[chan eof $channel]} {
chan close $channel
exit
} elseif {![chan blocked $channel]} {
if {[string match "update_text*" $cmd]} {
global status_text
set first [expr {[string first "(" $cmd] + 1}]
set last [expr {[string last ")" $cmd] - 1}]
set status_text [string range $cmd $first $last]
}
}
}
set server_socket [socket -server _ipc_server -myaddr localhost 0]
set server_port [fconfigure $server_socket -sockname]
set env(_PYIBoot_SPLASH) [lindex $server_port 2]
image create photo splash_image
splash_image put $_image_data
unset _image_data
proc canvas_text_update {canvas tag _var - -} {
upvar $_var var
$canvas itemconfigure $tag -text $var
}
package require Tk
set image_width [image width splash_image]
set image_height [image height splash_image]
set display_width [winfo screenwidth .]
set display_height [winfo screenheight .]
set x_position [expr {int(0.5*($display_width - $image_width))}]
set y_position [expr {int(0.5*($display_height - $image_height))}]
frame .root
canvas .root.canvas \
-width $image_width \
-height $image_height \
-borderwidth 0 \
-highlightthickness 0
.root.canvas create image \
[expr {$image_width / 2}] \
[expr {$image_height / 2}] \
-image splash_image
wm attributes . -transparentcolor magenta
.root.canvas configure -background magenta
pack .root
grid .root.canvas -column 0 -row 0 -columnspan 1 -rowspan 2
wm overrideredirect . 1
wm geometry . +${x_position}+${y_position}
wm attributes . -topmost 1
raise .�PNG

   IHDR  �   Q   	�   sRGB ���   gAMA  ���a   	pHYs  �  ��o�d   !tEXtCreation Time 2023:07:24 14:45:47`��L  �IDATx^�	�m���5׭ۨA���2Gn�%�B��d���E�9)R$"�������ԕ��$��͚��{�Z�{�o�}��g�w�}����Ϸ�w��眽�Z�ւ�� �B����B!�	l!��H`!�=@[!���B!D��B!z��B�$��B� �-�B� 	l!��H`!�=@[!���B!D��B!z��B�$��B� �-�B� 	l!��H`!�=@[!���B!D��B!z��B�$��B� �-�B� 	l!��H`w�7���p�����!,Z�!��N�h<I!�hǂ���/���_��G����8�q�~�x0��.�;��6!��v�L¸��[��_���Wǃ!U��?�p���`H��&��ӝ�{���C���xP�-�:����mo���]�ᇇ�o�p�5��B�{��B�z�xR�omr�n�9��/�C���2PZ���x�h��c�_�:�׫��Cx~�ǃ1p}>'�������3��/���Va�M�A&����~ѷs���`��1���7}&�[W\M�S��^��������Ž�?�6�[�d����V���Zk08��x�n���U��[o=�sN�@&|���5�N<1^�p������w����6�d���_�dŊ��s���e��sr�E��=�,�O�?~0Xc��k�m�5����o���Sf^c���r��{�<3�0!��3z]�]xa<)�]w-�_�un�!��w�s��6�8��W��k�s|��9i��x`<!��ҥ��1�t��{�ݶ�}._>z�ݎ9&��}��/��w^<)���+�N�X��|����m���s������g��Ń
v�!�]v��c�KBx�C�l�~���BOA�uT��䵯�;�B��}��`5~��!��V�~u�g&w�[�M7�Tp�!,]�]��_��ِ��
�ߍSȡ�Ɲ~�ۢ}���/���sܩ�W�*<�[�:��~5TPf]���3�AKhg��SN�;�v���j��z5,o~sܙE� >�i!��f��W�g��n���lY<� ��;�f���=�{�+��~6�c����5�y��u�BU0p[��]�P��Cx���?�p�;�L(i�RX����F���U�`
�җ����r�˹�5
����N��,\c\�~׻�N	��'�.^xa�}o<��;���9|��qgBN:�Z�a\�+P�6ݴwB[�OxBܩ���!:	�R���qn�U!�]w4.��>����,b�xr�< ��C:(���.DV��; P-��wj ���|��Wn�}l;�X�x��=��WB����?*�}��̶�2�]w�9�	�)O)�����8�x��L<��Rr�u�1i��Ǉ�Ǥsc�X�X�r������n·�j���N	��O�-��E)���VY$��|y�_��$L��&���q��*�;r 軾??�!�p.S�S�Dt��\.��<6b�M7.�,�!���G�W_]�0��n����l�Q}�ǰ��^}|q&�a��I��w|a��|�����^�q�E|о�m��	%���KY��:k0�r˙�){���vڸָ�9W1��6+�8�1�{K��<�-f��};��V���� �m�]�8�0��9$�91��}��>8�T�$1lڢ7��7�Xòe+��x��`��V��ư���x��}��Ĕm���xr~� _��#��Yg�=l�ٞ �){�w*@��J�&�,�E��!�zja��V\�ozS<��['�wm~�qg�|�;�)'�{����B��u�:�y}�!�W���Ź����D��)x%�9&�3{��z�Ń!�xGܩ��N�����T񑏌ZP��*7�~w�`�����?������Eƿe\B.|��!�\h�T'$�M�s�������*��7F=O��_8�ejW���<0�����_���3�H`7Ŗ-�Ayq.�f�"����}����V������#t�´[�� h���'>q|
���N���=�����#�N�![�4.������<��3CU<�A3���Ol��g���A6�{�R��l����)3k
��������{\����Yu���3όCP<ۆ���ݏ��7ei	��l���@�����qg����k�A�.��8%�z.-V,���}TkDp��M#6oQ���|�*q�.�0��)n�w"d��*oX.���D-��w�x0�1���{�#G�C]5ÑG��* ĨXc��8����?∸3�>�ַƃ1��qgJ� �#A��m �R������$�#��=l����މ]3G�����o_7��C�J,�U�`��֟���_��UW`��A���ith�d(�!1�䓋�$}�ˋsж(�`b	&�H��c1xWi���p�5��Qvd���_����ĝ
ؼK�
�.(�j��k�+
D�o2�ns\�9�	�5��;j9|�c�Kĺ��+�>S+0=dI�g��r]�{՟ϽI�
����O<��g�3�I�HJd�i
V>ބ{�3�cJ.ܮ���H�K��]���xKP.�p��	���z5��Ѷ���ĝYb\`�Y�6��o���N�����V��G��'��g���O}j�|���s�kf����Cx��������L(�e��(��G?�;=�r+���K�v��˹���N���+H��?ǝH�X�oW�W�uSm��Ff{ko�ܪM /��
s��m�:'�]ʫ���� �X�����*�N��i�x0�{_��6�WF RA�0���F�Ү@8>���`�aY�0h����s�%d6�@��3��������P��jl�@�I^8Q�
�������:$* 18�"�J�B!N-���\�<9�$��ܚ6���� ��-X*]B}-�V�w�q���MX+&/�DQǁ��;
��^��������Y�5@Xٸ������g��N�jm)�7�}��Oŝ!(k�ޝϲV=�Ǹ	�<(x!mX��t��\�� ���$�)�}[=����G	�Zk�s^�����ϔ/{Yܙ~�/����r�̪$����AgO�OtF�$y���-�t6��$�~9�4^G4��m���賲��2~����s�V%�!T����b?�g����c���t����
�*�s��b]�����$�#Ԝ[�V&�H�K�/I&m��B67nW��\�eH8�W�<��qg�����о����b!%�F�)�i�%*��&�5�v~w�q ��&�^���Wnn��.A��/�%�����%q���&���>�.��Cx�ˋ��A���w
aH�����}I�\��g��f����z�������:/V����L�U�e��E�k�����(V`2�b-�l܎M�(RMQ2ĭ������5(6��y��j�T�@Y���2>�6�}�M�����'.�g�xE�@ٰV6m��O�p�G�,��_�;Cz�R.�C[��x��}�Q�Z������&���Hh�[�s=��W`3%��%X̒D�f���d�g4�r��)�
;@%|��h���T�d���Ԣ��8		� ��O4��<���3�yo���r�b��e�3��6��պ���`�������(��V1z���NK���p�B�)�����nY��u�3�����U��?vf��1|BhVi��CO��q��a�Ɛ��@kt`��x-ɒ���b���G<B���7�_��v��:�$v�j���=��>��b��IRrkEg�������A��n�K(q��2V��`���1am��5�WYv��s��+����¤+V ! �d/w	�\�w�U+�%�r.�i�(���5)��\�dU�
�*Ϡ-dPc&\�z�V��|�{D{��܇�x&>G�	�w�p���d��~(k�w	����{&��b��du�:{�Ӌ���6��F&86�7����$6e9�oP�ʉ��ذ�RB�|�]�t�+��lG('u�\��C���,`/��$�/%��6�e�w��f�m�?*����M�H���&���'�`l3��(��g��#�y��B]MzC��L�$#8W!����(�U}�N����gAk
�X/}����w���N�  H}�e.(<���֭{h�V�mǦ]�mn�����5����
�O,6:>�6m��rC{���o�OB �*�A�N���̢K��5��6�X���:H�Pv
�,>���hkq��rp�д�wiê��65������Zg9����d*���}��2���;�&��XU6Y�:q��i˹��%�z^���[��]�>O��㲴�I,b�;	�	�+yqM����u�g	J(��hW��d�`b�6i�.�ςU����=鿶?�-SWw>��S`�9IC�rKe$G`q�� n�P����@�DrA�mlG������5Z5WwĘ��GIH�$�uC�V^9b`�rl�M�~�ER��x�6�׈�+n�Kl;�)� f��+�+�x���� W�B���o(�4���I��D鲊 71JNWB��6���	�847���$�>�����Ɇ�h�Mʻ(U�Pn��4�F���􋣏.�n[��Xi��?e���P�K�j]��_��f������)[���X���jZ�z+V���U�خ�*�P�_�������g5�v�/���C��MVo�N}?�]]ye|��W�:��������R�0ŊE��d�?[�u�xc|!r�qE{K�_~yq_�jM����U��U�%��۾���r��k����#^�{.���=g8��sYi��oW�j�Z��Y��b0Xwݕ��2�)ݷ�מ���R:��j,�O���M����j]U+�v��Uߖ.�/��~�`/}i�}u������E�(g=Vb�6w������j�}��S� ����&�[���$�q.nr,�ұ�r9꨸���\��~;(V?�	����9l�j �Q���,��bR�����ă	 Lg'���ϊY�&irE��%AY 	s�1֕Łs`�I�hC�gTN���i������v5�,�X���R���C,i� ���ˈ��J��L�j&t$P��k��@)�0ԸN��$sy����r_l��K�ă!�K;Z�)(�6���oNÂ%	���@<��9>���3��%4Va+nXK�Ǝ�-'\�E��n��iyW��6DHƇ{@6�����`����J
���◕%�d�Skh!C�k�s> ��&�P��F����F9Pq����L��2h�a�"Y�x�8�0�*!X>T?t�!)>|�I�I�ql��}�s9��8���� o�n�|�&J2�q�I�]��V�v҅K�R|���5���N���BٽKk �q�礐��==�B�8+i		�d�2(R�@�ENBץm��dV\wv�g`&y�	��]2�@b��(L^�"�d6�SL�����zh܉0�߯n�,�U��sLkg���In�,��>�E�uW��g	)�Dy��H�sdӯ�޳�8��D3�e�#8)�j�#��*c-m��ǲ{�6J���7]%��|�{H)�4̵߀~l@����p�PF@��e8Nh񠱂�J;���q��ĊN��Q�xqQcN��ߛi�t2�i���M���L Q�~�Ue���,/����r����kq�?�����iy.h�$�~d!`~3�Җ� m�Xb�`!��']�>k��[�6�xE܉4�A��m�.b�]�a]��,��`��ʩ�bMh&��)�����o�j���؀���u�
�Z�*�A`�����h�l$qc"6VV���M�A��6�r���F.{���8#���OV([�]������ێ�v� 	�j�|g�<^B9ԋ2iϲeų����s��Ĥ t&��x�e�͆曔+��8 d�'�颼+�2>[�.B��Iʹ�ǲ��AL�+��Zo}�ii-�眐Ք�jl 1���fР&�\N�����O�4ִU�����\�P��HR���{�'�G��3f�=���n�o,d���u��F<����t�9"T'Yư���u�]�D=V��>�Wmx6>L�#��	���8���o���ky���J[d!�6`Y����s!�+u])��x+{�,�SĪ#�!�\E�)��w� ����,QP�l�Ҹ :��L���1�J␾dg�S�Y ��]U)s�&�*o���=M{�o�xPe,��8>���9����e�������m���_���Na,�+\duw�e�nz�8�͙ �'�N��h�lr"xOW[����A�Y��~�Y@1v��]cۃ��;�.#���L�Iܻ��c;�?�`�[oX�q���}M3���u|�x�{F��XI(���_�v6ς�tn���� N��v71<B��Ro���[����|�\�V�¾_x�'���ǃ!��X��j��b���A�.JQwMY��X�aR� �N3ԡ��Dfk�s �ac��mک���#Yy��ˁP�]���۪��Gp����{M�7�<H9bUi(�i�B��ms{Pze%���RF2����\j/	�kɳ`S�4˄@w�m�]���O!�B!DX�\�B!�*��B�$��B� �-�B� 	l!��H`!�=@[!���B!D��B!z��B�$��B� �-�B� 	l!��H`!�=@[!���B!D��B!z��B�$��B� �-�B� 	l!��H`!�=@[!��zB��y��"L!    IEND�B`�